def bytes_to_video(bytes, 
                   filename: str = "animation.mp4"):

    with open(file = "tutorbot/assets/{filename}".format(filename = f"videos/{filename}"), 
              mode = 'wb') as video_file:
        
        video_file.write(bytes)