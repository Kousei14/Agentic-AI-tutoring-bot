from vertexai.preview.vision_models import ImageGenerationModel
import vertexai

import os
from dotenv import load_dotenv

load_dotenv()

vertexai.init(project = os.getenv("PROJECT_ID"), 
              location = os.getenv("LOCATION"))

generation_model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-preview-06-06")

images = generation_model.generate_images(
    prompt = "Craft a detailed image generation prompt for a manim-style illustration of a related rates calculus problem. The image should depict a conical tank with a black background and must not include any title text or extraneous words at the top. The illustration needs to include labels for the tank's height (H=6m) and radius (R=2m). It must also show blue water inside the tank, with the water level clearly labeled with height 'h = 4m' and radius 'r'. The overall style should be consistent with the clean, vector-graphics aesthetic of the Manim library. Ensure all labels are clear and mathematically accurate.",
    number_of_images = 1,
    aspect_ratio = "16:9",
    negative_prompt = "",
    person_generation = "allow_all",
    safety_filter_level = "block_few",
    add_watermark = True,
)

print(images.images[0]._image_bytes)