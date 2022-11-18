from synthesium.entity.entity import Entity
from synthesium.entity.point import Point
from synthesium.mutator.mutator import Mutator
from synthesium.mutator.timestamp import TimeStamp
from synthesium.utils.useful_functions import constant

"""some predefined Mutators"""


# TODO sort these into folders
class Show(Mutator):
    def __init__(self, target: Entity, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func=rate_func)

    def tick(self):
        super().tick()
        return self.target


class Move(Mutator):
    """Shifts are done by adding a tuple of length 2, in the form (x movement, y movement). Use negatives for left and down, respectively."""

    def __init__(self, target: Entity, amount: tuple, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.amount = amount

    def tick(self):
        super().tick()
        single_frame_amount = [amt / self.total_frames for amt in self.amount]
        adjusted_frame_amount = [amt * self.rate_func(self.current_frame, self.total_frames) for amt in
                                 single_frame_amount]
        return self.target.shift(tuple(adjusted_frame_amount))


class Rotate(Mutator):
    def __init__(self, target: Entity, degrees: int, center: Point, start: TimeStamp, end: TimeStamp,
                 rotates_clockwise=True, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.degrees = degrees
        self.center = center
        self.rotates_clockwise = rotates_clockwise

    def tick(self):
        super().tick()
        self.target.rotate(self.degrees / self.total_frames * self.rate_func(self.current_frame, self.total_frames),
                           self.center, rotates_clockwise=self.rotates_clockwise)
        return self.target


class MovePoint(Mutator):
    """Shifts are done by adding a tuple of length 2, in the form (x movement, y movement). Use negatives for left and down, respectively."""

    def __init__(self, target: Entity, point_index: int, amount: tuple, start: TimeStamp, end: TimeStamp,
                 rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.point_index = point_index
        self.amount = amount

    def tick(self):
        super().tick
        single_frame_amount = [amt / self.total_frames for amt in self.amount]
        adjusted_frame_amount = [amt * self.rate_func(self.current_frame, self.total_frames) for amt in
                                 single_frame_amount]
        self.target.points[self.point_index].shift(tuple(adjusted_frame_amount))
        return self.target


class Transform(Mutator):
    def __init__(self, target: Entity, attribute: str, end_attribute, start: TimeStamp, end: TimeStamp,
                 rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.attribute = attribute.lower()
        self.end_attribute = end_attribute
        self.start_attribute = getattr(target, attribute)
        self.should_call_pre_tick = True

    def pre_tick(self):  # in order to ensure that the transform acts on the most recent version of the target Entity,
        # initialization occurs right before ticking starts. This allows multiple Transforms to target the same Entity
        # as long as they aren't concurrent.

        start_attribute = getattr(self.target, self.attribute)
        self.difference = self.end_attribute - start_attribute

    def tick(self):
        super().tick()
        self.target.__setattr__(self.attribute, getattr(self.target,
                                                        self.attribute) + self.difference / self.total_frames * self.rate_func(
            self.current_frame, self.total_frames))
        return self.target
