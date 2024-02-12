import moviepy.editor as mp


#downScale a video 
def downScale(video_path, file_name):
    videoClip = mp.VideoFileClip(video_path)
    scale_fator = 0.3
    videoClip_resized = videoClip.resize(scale_fator)
    video_path = './static/data/' + 'lowResolution' +  file_name 
   
    videoClip_resized.write_videofile(video_path, audio_codec='aac')
    videoClip.close()
    videoClip_resized.close()
    return video_path