import boto3
import logging
from dotenv import load_dotenv
import os
import json

load_dotenv()
#initialize s3 resource
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='eu-north-1'
)

def uploadVideo(video_name,video_key):
    s3 = boto3.client('s3', region_name='eu-north-1') 
    bucketName = 'pipelinevod-nyatsikor-group'
    s3.upload_file(video_name, bucketName, video_key)
    

def uploadMetadata(metadatafile):
    dynamodb = session.resource('dynamodb', region_name='eu-north-1')
    table = dynamodb.Table('MetadataVoD')
    table.put_item(Item=metadatafile)


# def linkMetadataToVideo(video_key, metadatafile):
#     metadatafile["video_key"] = video_key
#     uploadMetadata(metadatafile)





    # If S3 object_name was not specified, use file_name
    
#intialize the dynamodb resource

def mainSend(metadatafile):
    logging.info(f"Sending data to AWS {metadatafile}")
    
    video_path = "data/" + metadatafile["fileName"]
    thumbnail_path = "data/" + metadatafile["thumbnail"]
    video_key = metadatafile["fileName"]
    thumbnail_key =  metadatafile["thumbnail"]
    
    

  
        
    uploadVideo(video_path,video_key)
    uploadVideo(thumbnail_path,thumbnail_key)
    uploadMetadata(metadatafile)
   
    
    return 'Upload successful'

# if __name__ == "__main__":
#     main()


# def send_data_to_aws(metadataFile):
    
