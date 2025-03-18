from dataclasses import dataclass, asdict
from typing import Optional
import numpy as np

@dataclass
class TileData:
    tile_image_path: str
    tile_bounds_latlon: dict
    pixel_bounds: dict
    homography: Optional[np.ndarray] = None

    def to_dict(self):
        return asdict(self)
    