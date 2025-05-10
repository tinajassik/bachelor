from ultralytics import YOLO
import os 

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
model_path = os.path.join(BASE_DIR, "car_detection_model", "best.pt")

model = YOLO(model_path)

async def detect(image_path):
    try:
        result = model.predict(image_path)
        return result
    except Exception as e:
        raise RuntimeError(f"Error during prediction: {e}") from e
