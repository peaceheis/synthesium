import copy

from synthesium.entity.vectorentity import VectorEntity
from synthesium.mutator.timestamp import TimeStamp
from synthesium.utils.useful_functions import constant


class Mutator:
    """Mutators make Entities change, and also return them for Canvas's renderer"""

    def __init__(
        self, target: VectorEntity, start: TimeStamp, end: TimeStamp, rate_func=constant
    ):
        self.current_frame = None
        self.should_call_pre_tick = False
        self.target = target
        self.validate_runtimes(start, end)
        self.start = start
        self.end = end
        self.rate_func = rate_func

    def tick(self) -> VectorEntity:
        self.current_frame += 1
        return self.target

    def get_start(self) -> TimeStamp:
        return self.start

    def set_start(self, marker: TimeStamp) -> "Mutator":
        self.validate_runtimes(marker, self.end)
        self.start = marker
        return self

    def get_end(self) -> TimeStamp:
        return self.end

    def set_end(self, marker: TimeStamp) -> "Mutator":
        self.validate_runtimes(self.start, marker)
        self.end = marker
        return self

    def is_active_at_frame(self, frame: TimeStamp):
        return self.start <= frame <= self.end

    def validate_runtimes(self, start: TimeStamp, end: TimeStamp):
        class InvalidRuntimeError(
            Exception
        ):  # here in the case an invalid runtime is encountered, i.e, end time < start time.
            def __init__(self):
                super().__init__(
                    f"Beginning time was set to {start}, \
                                        but end time was set to {end}"
                )

        if not start < end:
            raise InvalidRuntimeError()

    def copy(self) -> "Mutator":
        return copy.deepcopy(
            self
        )  # allows for creating small variants of a Mutator with method chaining

    def __str__(self):
        return f"Mutator of type {type(self)}"

    def __repr__(self):
        return f"{self.__class__.__name__}"
