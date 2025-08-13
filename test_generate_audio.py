from google import genai
from google.genai.types import (GenerateContentConfig, 
                                SpeechConfig, 
                                VoiceConfig, 
                                PrebuiltVoiceConfig)
import wave
from dotenv import load_dotenv

load_dotenv()

def wave_file(filename,
              pcm,
              channels = 1,
              rate = 24000,
              sample_width = 2):
    
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

client = genai.Client()

response = client.models.generate_content(
    model = "gemini-2.5-flash-preview-tts",
    contents = "Say in an informative manner: Hello! Today is Saturday. Have a wonderful day!",
    config = GenerateContentConfig(
        response_modalities = ["AUDIO"],
        speech_config = SpeechConfig(
            voice_config = VoiceConfig(
                prebuilt_voice_config = PrebuiltVoiceConfig(
                    voice_name = 'Sadaltager',
                )
            )
        ),
    )
)

data = response.candidates[0].content.parts[0].inline_data.data

file_name = 'sample.wav'
wave_file(file_name, data)
print(f"Audio saved to {file_name}")