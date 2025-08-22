from moviepy import VideoFileClip


def extract_audio_from_video(video_path: str = None,
                             audio_output_path: str = None):
    
    clip = VideoFileClip(video_path)
    
    clip.audio.write_audiofile(audio_output_path)
