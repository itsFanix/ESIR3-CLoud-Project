from flask import Flask, render_template, request, redirect, url_for
import  controller 



app = Flask(__name__)

@app.route('/')
def index():
    video_list = controller.get_video_list()
    print(video_list)
    return render_template('index.html', video_list=video_list)
    
@app.route('/playmedia', methods=['GET'])
def play():
    video_name = request.args.get('video_name')
    video_path = "./static/localStorage/" + video_name + ".mp4" 
    return render_template('playmedia.html', video_path=video_path)
if __name__== '__main__':
    app.run(debug=True)
