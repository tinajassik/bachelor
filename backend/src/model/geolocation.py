from dataclasses import dataclass, asdict

@dataclass
class GeoLocation:
    longitude: float
    latitude: float
    map_url: str

    def to_dict(self):
        return asdict(self)
    