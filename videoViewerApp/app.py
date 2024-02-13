from flask import Flask, render_template, request, redirect, url_for

import  controller 



app = Flask(__name__)

@app.route('/')
def index():
    video_list = controller.get_videoMetadata_list()
    return render_template('index.html', video_list=video_list)
    
@app.route('/playmedia', methods=['GET'])
def play():
    video_name = request.args.get('video_name')
    video_path, language, animals = controller.get_video(video_name)

   
    return render_template('playmedia.html', video_path=video_path, language=language, animals= animals)
if __name__== '__main__':
    app.run(debug=True)
