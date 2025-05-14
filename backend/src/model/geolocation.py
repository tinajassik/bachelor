from dataclasses import dataclass, asdict
from typing import List, Tuple

@dataclass
class GeoLocation:
    longitude: float
    latitude: float
    map_url: str

    def to_dict(self):
        return asdict(self)

@dataclass
class GeoLocations:
    geolocations: List[Tuple[float,float]]
    map_url: str

    def to_dict(self):
        return asdict(self)