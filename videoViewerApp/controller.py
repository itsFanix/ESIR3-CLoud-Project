import boto3  
import config
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

S3ressources = boto3.resource(
    's3',
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.REGION_NAME
)


dRessources = boto3.resource(
    'dynamodb',
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.REGION_NAME
)



def insertsubstitle(subtitles, video_path):
    return 'inserted'


def get_video_list():
    bucketName = 'pipelinevod-nyatsikor-group'
    bucket = S3ressources.Bucket(bucketName)
    video_list = []
    
    # print(response)
    for obj in bucket.objects.all():
        response = S3ressources.Object(bucketName, obj.key).get()
        res ={}
        res['name'] = obj.key.replace(".mp4",'')
        res['date'] = response['LastModified'].strftime("%Y-%m-%d") 
        video_list.append(res)
    print(video_list)

        # videopath = "localStorage/" + obj.key
        # S3ressources.Object(bucketName, obj.key).download_file(videopath)      
    return video_list




