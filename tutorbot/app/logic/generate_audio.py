from mutagen.mp3 import MP3
import wave
from typing import Literal

from tutorbot.assets.models.AudioGeneration import AudioGenerationModels

class AudioGeneratorAgent:
    def __init__(self):
        pass

    def generate(self,
                 script: str,
                 filename: str,
                 mode: Literal["gemini_tts", "default_tts"] = "default_tts",
                 model: str = "gemini-2.5-flash-preview-tts"):
        
        audio_model = AudioGenerationModels(
            mode = mode,
            model = model
        )

        # Generate data
        data = audio_model.generate(
            script = script
        )

        # data -> wav / mp3
        if mode == "gemini_tts":
            self.save_wave_file(
                filename = filename,
                pcm = data
            )

        elif mode == "default_tts":
            self.save_mp3_file(
                filename = filename,
                data = data
            )
        
        # Return duration
        return self.get_tts_duration(
            filename = filename,
            mode = mode
        )

    def save_wave_file(self,
                       filename,
                       pcm,
                       channels = 1,
                       rate = 24000,
                       sample_width = 2):
    
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)

    def save_mp3_file(self,
                      filename:str,
                      data):
        
        data.save(filename)

    def get_tts_duration(self, 
                         filename: str,
                         mode: Literal["default_tts", "gemini_tts"] = "default_tts") -> float:
        
        if mode == "gemini_tts":
            return self.get_wav_duration(filename)
        elif mode == "default_tts":
            return self.get_mp3_duration(filename)

    def get_wav_duration(self,
                         filename: str):
        
        try:
            with wave.open(filename, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                duration = frames / float(rate)
                return duration
        except wave.Error as e:
            print(f"Error opening or reading file: {e}")
            return None
        
    def get_mp3_duration(self,
                         filename: str):
        
        try:
            audio = MP3(filename)
            duration = audio.info.length
            return duration
        except Exception as e:
            print(f"Error reading MP3 file: {e}")
            return None

    