from PIL import Image
import io
import numpy as np
from services import skraafoto

def extract_selected_image(item_json): 
     props = item_json["properties"]
     return  props["asset:data"]

def convert_img_to_byte_array(img_url): 
    img = Image.open(io.BytesIO(skraafoto.get_image_from_url(img_url).content))
    return np.array(img)

def get_image_params(img_url):
    return np.array(Image.open(io.BytesIO(skraafoto.get_image_from_url(img_url).content))).shape

def convert_tiff_to_jpeg(file_path) -> bytes:
    """
    Converts a TIFF image from the given file path to JPEG format.
    Returns the JPEG image as raw bytes.
    """
    with Image.open(file_path) as img:
        img = img.convert("RGB")
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return buffer.getvalue()
