from videoProcessing import downScale
from flask import Flask, render_template, request, redirect, url_for

import os
import pika
# from videoProcessing import downScale

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    #RabbitMQ connection
    # connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    # channel = connection.channel()
    # channel.queue_declare(queue='videoNameQueue')

    # Request handling
    if request.method =='POST':
        #Vérification de la présence d'un fichier
        if 'video' not in request.files:
            return redirect(request.url)
        file = request.files['video']
        if file.filename =='':
            return redirect(request.url)
       
        #Enregistrement du fichier téléchargé
        file_path ='./static/uploads/' + file.filename
        file.save(file_path)
        #Downscaling the video
        processed_video_path = downScale(file_path, file.filename)
        #Suppression du fichier téléchargé
        os.remove(file_path)

        #Send the processed video name to the queue
        video_filename = processed_video_path.split('/')[-1]
        print("TEST MY VIDEO NAME")
        print(processed_video_path)
        print(video_filename)
        #Pour docker
        # channel.basic_publish(exchange='', routing_key='videoNameQueue', body=video_filename)
        # connection.close()
        return render_template('result.html', video_path=processed_video_path)
    
if __name__== '__main__':
    app.run(debug=True)
