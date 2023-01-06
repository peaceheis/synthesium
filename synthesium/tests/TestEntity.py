from typing import Tuple, Any

import numpy as np

from synthesium.entity.entity import Entity
from synthesium.mutator.timestamp import TimeStamp


class TestEntity(Entity):
    def __init__(self, x_size, y_size, color: float, *mutators):
        super().__init__(*mutators)
        self.x_size = x_size
        self.y_size = y_size
        self.color = color

    def render(self, active_frame: TimeStamp, fps: int) -> np.ndarray:
        arr = np.ndarray((self.x_size, self.y_size))
        arr.fill(self.color)
        return arr

    def get_top_left_coords(self) -> tuple[int, int]:
        return 0, 0

    def get_size(self) -> tuple[int, int]:
        return self.x_size, self.y_size
