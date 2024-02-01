import time
import math 

import ffmpeg

from faster_whisper import WhisperModel

from iso639 import Lang


input_video = "data/processaivoices2_2.mp4"
input_video_name = input_video.split("/")[-1].replace(".mp4", "") # remove .mp4


def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio


def transcribe_audio(audio):
    model = WhisperModel("base")
    segments, info = model.transcribe(audio)
    language = info[0]
    language = Lang(language).name
    print("Transcription language ", language)

    segments = list(segments)
    for segment in segments:
            #print(segment)
        print("[%.2f - %.2f] %s" % (segment.start, segment.end, segment.text))
    return language,segments


def run():
    extracted_audio = extract_audio()
    language, segments = transcribe_audio(audio=extracted_audio)


run()
