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
