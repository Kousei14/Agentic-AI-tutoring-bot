import cv2
from typing import Any
from manim import ImageMobject

def bytes_to_video(bytes, 
                   filename: str = "animation.mp4"):

    with open(file = "tutorbot/assets/{filename}".format(filename = f"videos/{filename}"), 
              mode = 'wb') as video_file:
        
        video_file.write(bytes)

def video_to_frames(video_path: str,
                    width: Any | None = None,
                    height: Any | None = None):
    
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    while True:
      ret, frame = cap.read()
      if not ret:
            break

      frame = cv2.resize(frame, 
                         (width, height))
      frame = cv2.cvtColor(frame, 
                           cv2.COLOR_BGR2RGB)

      frame_mobj = ImageMobject(frame)
      frames.append(frame_mobj)

    cap.release()

    return frames