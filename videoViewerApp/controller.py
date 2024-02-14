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

def insertsubstitle(subtitles, video_path):
    return 'inserted'

# video_list = []

video_metadata_list = {}

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

    for elmt in response['Items']:
        #recupère le lien du thumbnail
        elmt_thumbnail_path =   s3_client.generate_presigned_url(
        'get_object', Params ={'Bucket': bucketName, 'Key': elmt['thumbnail']})

        # S3ressources.Object(bucketName, i['thumbnail']).download_file(thumbnail_path)
        elmt['thumbnail'] = elmt_thumbnail_path
        elmt['duration'] = format_time(float(elmt['duration']))
        video_metadata_list[elmt['fileName']] = elmt
    return video_metadata_list


def get_video(video_name):
    bucketName = 'pipelinevod-nyatsikor-group'
    try:
        video_path = s3_client.generate_presigned_url(
        'get_object', Params ={'Bucket': bucketName, 'Key': video_name}
    )
    except ClientError as e:
        logging.error(e)
        return None
    

    video_metadata = video_metadata_list[video_name]
    substitles = video_metadata['subtitles']
    language = video_metadata['language']
    animals = video_metadata['animals']
    # for i in video_list:
    #     if i['fileName'] == video_name:
    #         substitles = i['subtitles']
    #         language = i['language']
    #         animals = i['animals']
    #         break
    return video_path,language,animals,substitles

