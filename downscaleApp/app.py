from videoProcessing import downScale
from flask import Flask, render_template, request, redirect, url_for

import os
import pika

import json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    #RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='videoNameQueue')
    channel.queue_declare(queue='metadataFileQueue')

    # Request handling
    if request.method =='POST':
        #Vérification de la présence d'un fichier
        if 'video' not in request.files:
            return redirect(request.url)
        video = request.files['video']

        videoDescription = request.form['videoDescription'] #Description de la vidéo

        thumbnail = request.files['thumbnail']   #Thumbnail de la vidéo

        if video.filename =='':
            return redirect(request.url)
        #téléchargement du thumbnail
       
        if thumbnail.filename =='':
            return redirect(request.url)
        
        #Enregistrement du fichier téléchargé
        video_path ='./static/uploads/' + video.filename
        # thumbnail_path = './static/uploads/' + thumbnail.filename
        thumbnail_name =video.filename.replace(".mp4","") +  "thumbnail.jpg"
        thumbnail_path = './static/data/' + thumbnail_name
        video.save(video_path)
        thumbnail.save(thumbnail_path)

        #Downscaling the video
        processed_video_path = downScale(video_path, video.filename)
        #Suppression du fichier téléchargé
        os.remove(video_path)
        

        #Send the processed video name to the queue
        video_filename = processed_video_path.split('/')[-1]
        print("TEST MY VIDEO NAME")
        print(processed_video_path)
        print(video_filename)

        metadata = {
            "fileName":  video_filename,
            "videoDescription": videoDescription,
            "duration": 0,
            "subtitles": "No subtitles available",
            "language": "No language detected",
            "thumbnail": thumbnail_name,
        }
        #Génération du metadata file
        json_metadata_file_path = f"./static/data/Metadata_{video_filename.replace('.mp4', '.json')}"
        with open(json_metadata_file_path, 'w') as json_file:
            json.dump(metadata, json_file)

        metadataFile = json_metadata_file_path.split("/")[-1]
        
        #Pour docker
        channel.basic_publish(exchange='', routing_key='videoNameQueue', body=metadataFile)
        connection.close()
        return render_template('result.html', video_path=processed_video_path)
    
if __name__== '__main__':
    app.run(debug=True)
