import math
import time
# Get a segment data and generate the substiles for it


input_segment = ""


def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds-math.floor(seconds))*1000)
    seconds = math.floor(seconds)

    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    return formatted_time



def generate_subtitles(video_name, segments):
    substite_file = f"sub-{video_name}.srt"
    text =""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text +=f"{str(index+1)} \n"
        text +=f"{segment_start} --> {segment_end} \n"
        text +=f"{segment.text} \n\n"
        text +="\n"

    with open(substite_file, "w") as f:
        f.write(text)
        f.close()
    return substite_file
