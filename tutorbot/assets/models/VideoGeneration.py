from google import genai
from google.genai.types import GenerateVideosConfig, Image

import time
import os
from dotenv import load_dotenv
load_dotenv()

class VideoGenerationModels:
    def __init__(self,
                 model: str = "veo-3.0-generate-001"):
        
        self.client = genai.Client(
            vertexai = True,
            project = os.getenv("PROJECT_ID"),
            location = os.getenv("LOCATION")
        )
        
        self.model = model

    def generate(self,
                 prompt: str,
                 image_path: str,
                 number_of_videos: int = 1,
                 aspect_ratio: str = "16:9"):
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at {image_path}")

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        reference_image = Image(
            image_bytes = image_bytes,
            mime_type = "image/png"
        )

        operation = self.client.models.generate_videos(
            model = self.model,
            prompt = prompt,
            image = reference_image,
            config = GenerateVideosConfig(
                number_of_videos = number_of_videos,
                aspect_ratio = aspect_ratio
            ),
        )

        while not operation.done:
            time.sleep(20)
            operation = self.client.operations.get(operation)

        return [generated_video.video.video_bytes for generated_video in operation.response.generated_videos]