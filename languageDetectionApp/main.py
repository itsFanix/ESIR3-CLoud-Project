import time
import math 
import ffmpeg
from faster_whisper import WhisperModel
from iso639 import Lang
import os
import pika
from retry import retry
import logging
import json



logging.basicConfig(level=logging.INFO)


#RabbitMQ connection
@retry(delay=5, backoff=2, max_delay=60,logger=None)
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    return connection

def extract_audio(video_name):
    input_video = "data/" + video_name
    input_video_name = input_video.split("/")[-1].replace(".mp4", "") # remove .mp4
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio


def transcribe_audio(audio):
    model = WhisperModel("base")
    segments, info = model.transcribe(audio)
    language = info[0]
    language =  Lang(language).name  if language != "nn" else "No language detected"
    segments = list(segments) if segments else list()
    os.remove(audio)
    return language,segments

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds-math.floor(seconds))*1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
    return formatted_time

def generate_subtitles(segments):
    substites = []
    text =""
    if not segments:
        return ["No subtitles available"]
    else:
        for index, segment in enumerate(segments):
            segment_start = format_time(segment.start)
            segment_end = format_time(segment.end)
            text +=f"{segment_start} --> {segment_end} : "
            text +=f"{segment.text}"
            subobject = {index : text}
            substites.append(subobject)
            text = ""
    return substites

def generate_metadata(video_name, subtitles, language):
    metadataDico = ffmpeg.probe("data/" + video_name)
    metadata = {
        "fileName":  video_name,
        "duration": metadataDico["format"]["duration"],
        "bit_rate": metadataDico["format"]["bit_rate"],
        "size": metadataDico["format"]["size"],
        "nb_streams": metadataDico["format"]["nb_streams"],
        "first_stream_codec_name": metadataDico["streams"][0]["codec_name"],
        "second_stream_codec_name": metadataDico["streams"][1]["codec_name"],  # ???? 
        "subtitles": subtitles,
        "language": language
    }

    logging.info(f"Metadata: {metadata}")
    json_metadata_file_path = f"data/Metadata_{video_name.replace('.mp4', '.json')}"
    with open(json_metadata_file_path, 'w') as json_file:
        json.dump(metadata, json_file)
    logging.info(f"Metadata file: {json_metadata_file_path}")
    return json_metadata_file_path.split("/")[-1]


def run(video_name):
    extracted_audio = extract_audio(video_name)
    language, segments = transcribe_audio(audio=extracted_audio)
    subtitles = generate_subtitles(segments)
    logging.info(f"Subtitles: {subtitles}")
    logging.info(f"Language detected: {language}")
    metadatafile = generate_metadata(video_name, subtitles, language)
    return metadatafile
    

def main():

    logging.info("########################GET LANGUAGE AND SUBSTITLES POD ################################")
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    # create a queue to receive the video name from the downscale app
    channel.queue_declare(queue='videoNameQueue')  
    channel.queue_declare(queue='metadataFileQueue')
    logging.info('Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        logging.info("########################################################")
        logging.info(f" Received   {body} ")
        metadataFile = run(body.decode('utf-8'))
        video_name = body.decode('utf-8')
        # channel.basic_publish(exchange='', routing_key='metadataFileQueue', body=video_name)
        channel.basic_publish(exchange='', routing_key='metadataFileQueue', body=metadataFile)

        logging.info("########################################################")
    channel.basic_consume(queue='videoNameQueue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    
if __name__ == "__main__":

    main()