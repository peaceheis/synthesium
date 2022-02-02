from synthesium.mation.timestamp import TimeStamp
from synthesium.utils.useful_functions import constant
from synthesium.mation.mation import Mation
from synthesium.matable.matable import Matable
from synthesium.matable.point import Point

"""some predefined Mations"""
#TODO sort these into folders
class Show(Mation): 
    def __init__(self, target: Matable, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func=rate_func)

    def tick(self): 
        super().tick()
        return self.target

class Move(Mation):
    """Shifts are done by adding a tuple of length 2, in the form (x movement, y movement). Use negatives for left and down, respectively."""
    def __init__(self, target: Matable, amount: tuple, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.amount = amount

    def tick(self): 
        super().tick()
        single_frame_amount = [amt/self.total_frames for amt in self.amount]
        adjusted_frame_amount = [amt * self.rate_func(self.current_frame, self.total_frames) for amt in single_frame_amount]
        return self.target.shift(tuple(adjusted_frame_amount))

class Rotate(Mation): 
    def __init__(self, target: Matable, degrees: int, center: Point, start: TimeStamp, end: TimeStamp, rotates_clockwise=True, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        self.degrees = degrees
        self.center = center
        self.rotates_clockwise = rotates_clockwise

    def tick(self): 
        super().tick()
        self.target.rotate(self.degrees/self.total_frames * self.rate_func(self.current_frame, self.total_frames), self.center, rotates_clockwise=self.rotates_clockwise)
        return self.target

class MovePoint(Mation): 
    """Shifts are done by adding a tuple of length 2, in the form (x movement, y movement). Use negatives for left and down, respectively."""
    def __init__(self, target: Matable, point_index: int, amount: tuple, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        self.point_index = point_index
        self.amount = amount

    def tick(self):
        super().tick
        single_frame_amount = [amt/self.total_frames for amt in self.amount]
        adjusted_frame_amount = [amt * self.rate_func(self.current_frame, self.total_frames) for amt in single_frame_amount]
        self.target.points[self.point_index].shift(tuple(adjusted_frame_amount))
        return self.target

class Transform(Mation): 
    def __init__(self, target: Matable, attribute: str, end_attribute, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        self.attribute = attribute.lower()
        self.end_attribute = end_attribute
        self.start_attribute = getattr(target, attribute)
        self.should_call_pre_tick = True

    def pre_tick(self): # in order to ensure that the transform acts on the most recent version of the target Matable,
        # initialization occurs right before ticking starts. This allows multiple Transforms to target the same Matable
        # as long as they aren't concurrent.

        start_attribute = getattr(self.target, self.attribute)
        self.difference = self.end_attribute - start_attribute

    def tick(self):
        super().tick()
        self.target.__setattr__(self.attribute, getattr(self.target,self.attribute) + self.difference/self.total_frames * self.rate_func(self.current_frame, self.total_frames))
        return self.target

class ChangeOpacity(Mation): 
    def __init__(self, target: Matable, opacity: float, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        assert 0 <= opacity and opacity <= 1
        self.opacity = opacity
        self.should_call_pre_tick = True

    def pre_tick(self): 
        self.start_opacity = self.target.get_opacity()
        self.difference = self.opacity - self.start_opacity

    def tick(self):  
        self.target.set_opacity(self.start_opacity + self.difference/self.total_frames * self.rate_func(self.current_frame, self.total_frames))

class ChangeOpacityFill(Mation): 
    def __init__(self, target: Matable, opacity: float, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        assert 0 <= opacity and opacity <= 1
        self.opacity = opacity
        self.should_call_pre_tick = True

    def pre_tick(self): 
        self.start_opacity = self.target.get_opacity_fill()
        self.difference = self.opacity - self.start_opacity

    def tick(self):  
        self.target.set_opacity_fill(self.target.get_opacity() + self.difference/self.total_frames * self.rate_func(self.current_frame, self.total_frames))

class ChangeRed(Mation): 
    def __init__(self, target: Matable, red_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        assert 0 <= red_val and red_val <= 1
        self.red_val = red_val
        self.should_call_pre_tick = True

    def pre_tick(self): 
        self.start_red = self.target.get_red()
        self.difference = self.red_val - self.start_red

    def tick(self):  
        self.target.set_red(self.target.get_red() + self.difference/self.total_frames * self.rate_func(self.current_frame, self.total_frames))

class ChangeRedFill(Mation): 
    def __init__(self, target: Matable, red_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        assert 0 <= red_val and red_val <= 1
        self.red_val = red_val
        self.should_call_pre_tick = True

    def pre_tick(self): 
        self.start_red = self.target.get_red_fill()
        self.difference = self.red_val - self.start_red

    def tick(self):  
        self.target.set_red_fill(self.target.get_red_fill() + self.difference/self.total_frames * self.rate_func(self.current_frame, self.total_frames))

class ChangeGreen(Mation): 
    def __init__(self, target: Matable, green_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        assert 0 <= green_val and green_val <= 1
        self.green_val = green_val
        self.should_call_pre_tick = True

    def pre_tick(self): 
        self.start_green = self.target.get_green()
        self.difference = self.green_val - self.start_green

    def tick(self):  
        self.target.set_green(self.target.get_green() + self.difference/self.total_frames * self.rate_func(self.current_frame, self.total_frames))

class ChangeGreenFill(Mation): 
    def __init__(self, target: Matable, green_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        assert 0 <= green_val and green_val <= 1
        self.green_val = green_val
        self.should_call_pre_tick = True

    def pre_tick(self): 
        self.start_green = self.target.get_green_fill()
        self.difference = self.green_val - self.start_green

    def tick(self):  
        self.target.set_green_fill(self.target.get_green_fill() + self.difference/self.total_frames * self.rate_func(self.current_frame, self.total_frames))

class ChangeBlue(Mation): 
    def __init__(self, target: Matable, blue_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        assert 0 <= blue_val and blue_val <= 1
        self.blue_val = blue_val
        self.should_call_pre_tick = True

    def pre_tick(self): 
        self.start_blue = self.target.get_blue()
        self.difference = self.blue_val - self.start_blue

    def tick(self):  
        self.target.set_blue(self.target.get_blue() + self.difference/self.total_frames * self.rate_func(self.current_frame, self.total_frames))

class ChangeBlueFill(Mation): 
    def __init__(self, target: Matable, blue_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant): 
        super().__init__(target, start, end, rate_func)
        assert 0 <= blue_val and blue_val <= 1
        self.blue_val = blue_val
        self.should_call_pre_tick = True

    def pre_tick(self): 
        self.start_blue = self.target.get_blue_fill()
        self.difference = self.blue_val - self.start_blue

    def tick(self):  
        self.target.set_blue_fill(self.target.get_blue_fill() + self.difference/self.total_frames * self.rate_func(self.current_frame, self.total_frames))