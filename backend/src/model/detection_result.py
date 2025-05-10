from dataclasses import dataclass, asdict
from typing import List
from model import GeoLocations

@dataclass
class Detection:
    class_id: int
    confidence: float
    bbox: List[float]  

@dataclass
class DetectionResult:
    file_name: str
    detections: List[Detection]
    labeled_image: str 
    projected_geolocations: GeoLocations

    def to_dict(self):
        return {
            "filename": self.file_name,
            "detections": [asdict(det) for det in self.detections],
            "labeled_image": self.labeled_image,
            "projected_geolocations": self.projected_geolocations.to_dict()
        }