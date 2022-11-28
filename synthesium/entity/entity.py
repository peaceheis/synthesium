import numpy

from synthesium.canvas import blendingfuncs
from synthesium.mutator.timestamp import TimeStamp


class Entity:
    def __init__(self, *mutators, blending_func: blendingfuncs.blendingfunc = blendingfuncs.normal):
        self.mutators: "list[Mutator]" = []
        self.visible_from: list[tuple[TimeStamp]] = []
        self.start: TimeStamp = TimeStamp()
        self.end: TimeStamp = TimeStamp()
        self.blending_func = blending_func

    def render(self, active_frame: TimeStamp, fps: int) -> numpy.ndarray:
        """A central method to Synthesium. Allows an Entity to render itself - when creating custom Entities, this
        method should be overriden.
        """
        pass  # TODO: Add context for if entity should be removed when finished

    def add_visibility_window(self, *windows: list[tuple[TimeStamp]]):
        for window in windows:
            if window[0] >= window[1]:
                raise ValueError("Improper viewing window provided to entity.")
        self.visible_from.extend(*windows)
        self.start = min(self.start, *[window[0] for window in windows])
        self.end = max(self.end, *[window[1] for window in windows])

    def active_at(self, frame: TimeStamp):
        if not self.start <= frame <= self.end:
            return False

        for window in self.visible_from:
            if window[0] <= frame <= window[1]:
                return True
        return False

    def tick(self, at: TimeStamp):
        for mutator in self.mutators:
            if mutator.is_active_at_frame(at):
                mutator.tick()

    def get_top_left_coords(self) -> tuple[int]:
        pass

    def get_size(self) -> tuple[int]:
        pass


def configure(default_config, **kwargs):
    """Configure works by taking in all the kwargs passed to init(), and comparing them against the default config. Anything new is updated,
       otherwise the defaults are used. This allows for the dynamic setting of attributes in one dictionary."""
    new_config = kwargs
    for key, value in new_config.items():
        default_config[key] = value  # update the default_config as necessary with new values
    return default_config  # while it returns "default_config," it's really returning the modified config.
