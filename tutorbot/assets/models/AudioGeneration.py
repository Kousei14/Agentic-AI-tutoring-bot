from google import genai
from google.genai.types import (GenerateContentConfig, 
                                SpeechConfig, 
                                VoiceConfig, 
                                PrebuiltVoiceConfig)

from typing import Literal
from gtts import gTTS
from dotenv import load_dotenv
load_dotenv()

class AudioGenerationModels:
    def __init__(self,
                 mode: Literal["gemini_tts", "default_tts"] = "default_tts",
                 model: str = "gemini-2.5-flash-preview-tts"):
        
        self.mode = mode
        self.model = model

        self.client = genai.Client()

    def generate(self,
                 script: str):
        
        if self.mode == "gemini_tts":
            return self.gemini_tts(script)
        elif self.mode == "default_tts":
            return self.default_tts(script)
        
    def default_tts(self,
                    script: str):
        
        data = gTTS(
            text = script
            )
        
        return data

    def gemini_tts(self,
                   script: str):

        response = self.client.models.generate_content(
            model = self.model,
            contents = f"Say in an informative manner: {script}",
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

        return data

    