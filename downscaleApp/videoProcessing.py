import moviepy.editor as mp


#downScale a video 
def downScale(video_path, file_name):
    videoClip = mp.VideoFileClip(video_path)
    scale_fator = 0.3
    videoClip_resized = videoClip.resize(scale_fator)
    output_path = './static/processVideo/' + 'process' +  file_name 
    # output_path = '../processDirectory/' +  file_name +'processed.mp4'
    videoClip_resized.write_videofile(output_path, audio_codec='aac')
    videoClip.close()
    videoClip_resized.close()
    return output_path