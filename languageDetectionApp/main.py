import time
import math 
import ffmpeg
from faster_whisper import WhisperModel
from iso639 import Lang
import os
import pika

from retry import retry




#RabbitMQ connection


@retry(delay=5, backoff=2, max_delay=60, logger=None)
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    return connection


def callback(ch, method, properties, body):
        print("########################################################")
        print(f" [x] Received   {body} ")
        # run(body.decode('utf-8'))
        print("########################################################")


def main():

    print("########################START ################################")
    
    connection = connect_to_rabbitmq()
    channel = connection.channel()

    channel.queue_declare(queue='donwscale_process')   

        # # receive the video name from the queue
    
    
    channel.basic_consume(queue='donwscale_process', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()






if __name__ == "__main__":
    print("#############START#########")
    # main()


# def extract_audio(video_name):
#     input_video = "data/" + video_name
#     input_video_name = input_video.split("/")[-1].replace(".mp4", "") # remove .mp4

#     extracted_audio = f"audio-{input_video_name}.wav"
#     stream = ffmpeg.input(input_video)
#     stream = ffmpeg.output(stream, extracted_audio)
#     ffmpeg.run(stream, overwrite_output=True)
#     return extracted_audio


# def transcribe_audio(audio):
#     model = WhisperModel("base")
#     segments, info = model.transcribe(audio)
#     language = info[0]
#     language = Lang(language).name
#     print("Transcription language ", language)

#     segments = list(segments)
#     for segment in segments:
#             #print(segment)
#         print("[%.2f - %.2f] %s" % (segment.start, segment.end, segment.text))
    
#     os.remove(audio)
#     return language,segments

# def run(video_name):
#     extracted_audio = extract_audio(video_name)
#     language, segments = transcribe_audio(audio=extracted_audio)



