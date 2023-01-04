from typing import Callable

import numpy as np

blendingfunc = Callable[[np.ndarray, np.ndarray], np.ndarray]

def normal(base_color: np.ndarray, blended_color: np.ndarray) -> np.ndarray:
    arr: np.ndarray = np.ndarray([4])
    base_red, base_green, base_blue, base_opacity = base_color
    blended_red, blended_green, blended_blue, blended_opacity = blended_color

    arr[0] = base_red * base_opacity + blended_red * blended_opacity
    arr[1] = base_green * base_opacity + blended_green * blended_opacity
    arr[2] = base_blue * base_opacity + blended_blue * blended_opacity
    arr[3] = 1 # TODO Change this back
    return arr
