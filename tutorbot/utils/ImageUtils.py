from PIL import Image
import io
import numpy as np

def bytes_to_image(bytes,
                   filename: str = "illustration.jpg"):

    pil_image = Image.open(
                fp = io.BytesIO(bytes)
                )

    image = pil_image.convert("RGB")
    image.save(
        fp = "tutorbot/assets/{filename}".format(filename = f"images/{filename}"), 
        format = "JPEG"
        )
    
def bytes_to_array(bytes):

    pil_image = Image.open(
        fp = io.BytesIO(bytes)
        )
    
    return np.array(pil_image)