from openai import OpenAI

import os
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

class TextGenerationModels:
    def __init__(self,
                 mode: Literal["gemini", "openai"] = "gemini",
                 model: Literal["gemini-2.5-flash", "gpt-4o-mini"] = "gemini-2.5-flash"):

        self.mode = mode
        self.model = model
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    def generate(self, 
                 prompt: str):
        
        if self.mode == "gemini":
            client = OpenAI(
                api_key = self.GOOGLE_API_KEY,
                base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            )

            response = client.chat.completions.create(
                model = self.model,
                reasoning_effort = "high",
                messages = [
                    {
                        "role": "system", 
                        "content": "You are a tutoring bot."},
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content
        
        elif self.mode == "openai":
            client = OpenAI(
                api_key = self.OPENAI_API_KEY,
            )

            response = client.chat.completions.create(
                model = self.model,
                store = True,
                messages = [
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content