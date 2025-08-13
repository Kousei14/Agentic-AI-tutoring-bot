import time
import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateVideosConfig, Image

load_dotenv()

client = genai.Client(
    vertexai = True,
    project = os.getenv("PROJECT_ID"),
    location = os.getenv("LOCATION")
)

# Specify the path to your local reference image
image_path = "reference.png"

# Check if the image file exists
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image file not found at {image_path}")

# Create an Image object from your local file
with open(image_path, "rb") as f:
    image_bytes = f.read()

reference_image = Image(
    image_bytes = image_bytes,
    mime_type = "image/png" # Adjust mime_type based on your image type (e.g., 'image/jpeg')
)

operation = client.models.generate_videos(
    model = "veo-3.0-generate-001",
    prompt = "Cinematic aerial shot of a red sailboat on a turquoise ocean, golden sunset, gentle waves",
    image = reference_image,  # Add the reference image here
    config = GenerateVideosConfig(
        number_of_videos = 2,
        aspect_ratio = "16:9"
    ),
)

while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)

for n, generated_video in enumerate(operation.response.generated_videos):
    video_bytes = generated_video.video.video_bytes

    with open(f"ocean_sailboat_{n}.mp4", "wb") as f:
        f.write(video_bytes)
    print(f"Saved video as ocean_sailboat_{n}.mp4")