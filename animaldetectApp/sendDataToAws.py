import boto3
import logging
from botocore.exceptions import ClientError
import os

#initialize s3 resource
s3 = boto3.client('s3', region_name='eu-north-1') 
bucketName = 'pipelinevod-nyatsikor-group'

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('metadataFile')


def uploadVideo(video_name, bucket, video_key):
    s3.upload_file(video_name, bucket, video_key)
    

def uploadMetadata(metadatafile):
    table.put_item(Item=metadatafile)


def linkMetadataToVideo(video_key, metadatafile):
    metadatafile["video_key"] = video_key
    uploadMetadata(metadatafile)


    # If S3 object_name was not specified, use file_name
    
#intialize the dynamodb resource




# def send_data_to_aws(metadataFile):
    
