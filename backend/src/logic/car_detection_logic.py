from object_detection import car_detector
from fastapi import File, UploadFile
import os, shutil
from model import DetectionResult, Detection
from utils import tile_splitter_stat
from logic import georeferencing_logic
import re 
from services import skraafoto

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
UPLOAD_DIR = os.path.join(BASE_DIR, "car_detection_model", "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "car_detection_model", "images_predictions")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def detect_cars(input: UploadFile = File(...)) -> DetectionResult: 
    input_path = os.path.join(UPLOAD_DIR, input.filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(input.file, buffer)

    results = await car_detector.detect(input_path)

    labeled_path = os.path.join(OUTPUT_DIR, input.filename)
    results[0].save(filename=labeled_path)

    detections = []
    bbox_central_points = []

    for r in results:
        xywhn = r.boxes.xywhn.tolist()
        h_orig, w_orig = r.orig_shape
        for box_data, center_n in zip(r.boxes.data.tolist(), xywhn):
            center_x_orig = center_n[0] * w_orig
            center_y_orig = center_n[1] * h_orig

            detection = Detection(
                class_id=int(box_data[5]),
                confidence=float(box_data[4]),
                bbox=box_data[0:4], 
            )
            detections.append(detection)
            bbox_central_points.append([center_x_orig, center_y_orig])
    
    stac_item_id = __get_item_id_from_tile_name(input.filename)
    bbox_central_points_original = __map_predicted_pixels_to_original_pixel(bbox_central_points, input.filename, stac_item_id)
    projected_geolocations = georeferencing_logic.get_geolocations_for_pixels(stac_item_id, bbox_central_points_original)

    with open(labeled_path, "rb") as img_file:
        labeled_bytes = img_file.read()

    result = DetectionResult(file_name=input.filename, detections=detections, labeled_image=labeled_bytes.hex(), projected_geolocations= projected_geolocations)
    os.remove(input_path)

    return result


def __map_predicted_pixels_to_original_pixel(predicted_pixels, file_name, stac_item_id):
    """
    Maps predicted central points of bounding boxes to the original STAC Item Skraafoto image. 
    Input: Predicted pixel location from a tile (a cropped tile from a Skraafoto image)
    Output: Transformed predicted pixel locations on the original Skraafoto image
    """
    mapped_pixel_locations = []
    img_height = skraafoto.fetch_skraafoto_item(stac_item_id)['properties']['proj:shape'][0]
    for prediction in predicted_pixels:
        mapped_pixel_location = tile_splitter_stat.find_pixel_position(tile_filename = file_name, pixel_x=prediction[0], pixel_y=prediction[1], image_height=img_height)
        mapped_pixel_locations.append(mapped_pixel_location)
    return mapped_pixel_locations

def __get_item_id_from_tile_name(tile_filename):
    parts = re.split(r'[-.]', tile_filename)
    return parts[0]