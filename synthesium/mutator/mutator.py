import copy

from synthesium.entity.entity import *
from synthesium.mutator.timestamp import TimeStamp
from synthesium.utils.useful_functions import constant


class Mutator:
    """Mutators make Entities change, and also return them for Canvas's renderer"""

    def __init__(self, target: Entity, start: TimeStamp, end: TimeStamp, rate_func=constant):
        self.current_frame = None
        self.should_call_pre_tick = False
        self.target = target
        self.validate_runtimes(start, end)
        self.start = start
        self.end = end
        self.rate_func = rate_func

        self.fps = None  # makes a lot of computation easier for this attribute to be here, instead of it being undefined until it gets
        # played() in a Canvas
        if self.fps is not None:
            self.total_frames = self.end.time_as_int(self.fps) - self.start.time_as_int(self.fps) + 1
        else:
            self.total_frames = None

    def overlaps(self, mutator: "Mutator"):
        """Check if the second mutator starts or ends before or when the first mutator ends, but starts after or when the first mutator starts, or vice versa.
        \nIn other words, check for overlap."""
        return self.get_end() >= mutator.get_start() >= self.get_start() \
               or \
               self.get_start() <= mutator.get_end() and self.get_end() >= mutator.get_start()

    def tick(self) -> Entity:
        """Tick gets called by Canvas to make the mutator advance by one frame: tick updates the `target` Entity, and updates
        the attribute self.current_frame, which is initialized ONLY after set_fps is called by Canvas, by the amount returned by the rate_function."""
        self.current_frame += 1
        return self.target

    def get_start(self) -> TimeStamp:
        return self.start

    def set_start(self, marker: TimeStamp) -> "Mutator":
        self.validate_runtimes(marker, self.end)
        self.start = marker
        return self

    def get_start_as_int(self) -> int:
        return self.start.time_as_int(self.fps)

    def get_end(self) -> TimeStamp:
        return self.end

    def set_end(self, marker: TimeStamp) -> "Mutator":
        self.validate_runtimes(self.start, marker)
        self.end = marker
        return self

    def get_end_as_int(self) -> int:
        return self.end.time_as_int(self.fps)

    def set_fps(self, fps):
        """Gets called in Canvas's internals when self.play(Mutator) is called, allowing for fps, necessary for tick(), to be set
           after instantiation"""

        assert (any([type(fps) == int, type(fps) == float]))  # make sure fps is a number
        if self.start.get_frame() > fps:
            raise Exception(f"Mutator's start frame is greater than FPS. ({self.start.get_frame()} > {fps})")
        if self.end.get_frame() > fps:
            raise Exception(f"Mutator's start frame is greater than FPS. ({self.end.get_frame()} > {fps})")
        self.fps = fps
        self.current_frame = 0
        self.total_frames = self.end.time_as_int(self.fps) - self.start.time_as_int(self.fps) + 1

    def get_range_of_frames(self):  # mostly for internal use
        return range(self.total_frames)

    def is_active_at_frame(self, frame):
        return self.start.time_as_int(self.fps) <= frame <= self.end.time_as_int(self.fps)

    def validate_runtimes(self, start: TimeStamp, end: TimeStamp):
        class InvalidRuntimeError(
            Exception):  # here in the case an invalid runtime is encountered, i.e, end time < start time.
            def __init__(self):
                super().__init__(f"Beginning time was set to {start}, \
                                        but end time was set to {end}")

        if not start < end:
            raise InvalidRuntimeError()

    def copy(self) -> "Mutator":
        return copy.deepcopy(self)  # allows for creating small variants of a Mutator with method chaining

    def __str__(self):
        return f"Mutator of type {type(self)}"

    def __repr__(self):
        return f"{self.__class__.__name__}"
