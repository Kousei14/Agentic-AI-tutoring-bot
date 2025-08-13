from vertexai.preview.vision_models import ImageGenerationModel
import vertexai

import os
from dotenv import load_dotenv
load_dotenv()

class ImageGenerationModels:
    def __init__(self,
                 model: str = "imagen-4.0-generate-preview-06-06"):

        vertexai.init(project = os.getenv("PROJECT_ID"), 
                      location = os.getenv("LOCATION"))

        self.generation_model = ImageGenerationModel.from_pretrained(
            model_name = model
            )

    def generate(self, 
                 prompt: str, 
                 number_of_outputs: int = 1, 
                 aspect_ratio: str = "16:9"):
        
        images = self.generation_model.generate_images(
                            prompt = prompt,
                            number_of_images = number_of_outputs,
                            aspect_ratio = aspect_ratio,
                            negative_prompt = "",
                            person_generation = "allow_all",
                            safety_filter_level = "block_few"
                        )

        return images.images[0]._image_bytes
