import boto3  
import config
from datetime import datetime
import math 
import ffmpeg
import logging
from botocore.exceptions import ClientError


session = boto3.Session(
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.REGION_NAME
)


s3_client = session.client('s3')
dynamodb_client = session.resource('dynamodb')
# dRessources = boto3.session(
#     'dynamodb',
#     aws_access_key_id=config.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
#     region_name=config.REGION_NAME
# )



def insertsubstitle(subtitles, video_path):
    return 'inserted'
video_list = []
def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds-math.floor(seconds))*1000)
    seconds = math.floor(seconds)
    # formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
    formatted_time = f"{minutes:02d}:{seconds:02d}"
    return formatted_time

def get_videoMetadata_list():
    dynamodbTable = dynamodb_client.Table('MetadataVoD')
    bucketName = 'pipelinevod-nyatsikor-group'
    response = dynamodbTable.scan()

    for i in response['Items']:
        thumbnail_path =   s3_client.generate_presigned_url(
        'get_object', Params ={'Bucket': bucketName, 'Key': i['thumbnail']})
        # thumbnail_path = "./static/localStorage/" + i['thumbnail']
        # S3ressources.Object(bucketName, i['thumbnail']).download_file(thumbnail_path)
        i['thumbnail'] = thumbnail_path
        i['duration'] = format_time(float(i['duration']))
        video_list.append(i)
    
    print(video_list)
    return video_list


def get_video(video_name):
    bucketName = 'pipelinevod-nyatsikor-group'
    # video_path = f"./static/localStorage/{video_name}"

    try:
        
        video_path = s3_client.generate_presigned_url(
        'get_object', Params ={'Bucket': bucketName, 'Key': video_name}
    )
    
    
    
    except ClientError as e:
        logging.error(e)
        return None



    # S3ressources.Object(bucketName, video_name).download_file(video_path)
    substitles = []
    substitles_path= f"./static/localStorage/{video_name}" + ".srt"
    language =""
    animalss =[]

    for i in video_list:
        if i['fileName'] == video_name:
            substitles = i['subtitles']
            language = i['language']
            animals = i['animals']
            break

    # with open(substitles_path, 'w') as file:
    #     for sub in substitles:
    #         print(sub)
    #         file.write(str(sub) + "\n")
        
    # video_input_stream = ffmpeg.input(video_path)
    # subtitle_input_stream = ffmpeg.input(substitles_path)
    # output_video = f"./static/localStorage/output-{video_name}.mp4"
    # subtitle_track_title = substitles_path.replace(".srt", "")


    # stream = ffmpeg.output(video_input_stream, output_video,
    #                            vf=f"subtitles={substitles_path}'",)

    # ffmpeg.run(stream, overwrite_output=True)
    
    
    return video_path, language, animals

