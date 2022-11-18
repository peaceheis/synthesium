from synthesium.entity.entity import Entity
from synthesium.mutator.mutator import Mutator
from synthesium.mutator.timestamp import TimeStamp
from synthesium.utils.useful_functions import constant


class ChangeOpacity(Mutator):
    def __init__(self, target: Entity, opacity: float, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.difference = None
        self.start_opacity = None
        assert 0 <= opacity <= 1
        self.opacity = opacity
        self.should_call_pre_tick = True

    def pre_tick(self):
        self.start_opacity = self.target.get_opacity()
        self.difference = self.opacity - self.start_opacity

    def tick(self):
        self.target.set_opacity(
            self.start_opacity + self.difference / self.total_frames * self.rate_func(self.current_frame,
                                                                                      self.total_frames))
        return self.target


class ChangeOpacityFill(Mutator):
    def __init__(self, target: Entity, opacity: float, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.difference = None
        self.start_opacity = None
        assert 0 <= opacity <= 1
        self.opacity = opacity
        self.should_call_pre_tick = True

    def pre_tick(self):
        self.start_opacity = self.target.get_opacity_fill()
        self.difference = self.opacity - self.start_opacity

    def tick(self):
        self.target.set_opacity_fill(
            self.target.get_opacity() + self.difference / self.total_frames * self.rate_func(self.current_frame,
                                                                                             self.total_frames))
        return self.target


class ChangeRed(Mutator):
    def __init__(self, target: Entity, red_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.difference = None
        self.start_red = None
        assert 0 <= red_val <= 1
        self.red_val = red_val
        self.should_call_pre_tick = True

    def pre_tick(self):
        self.start_red = self.target.get_red()
        self.difference = self.red_val - self.start_red

    def tick(self):
        self.target.set_red(
            self.target.get_red() + self.difference / self.total_frames * self.rate_func(self.current_frame,
                                                                                         self.total_frames))
        return self.target


class ChangeRedFill(Mutator):
    def __init__(self, target: Entity, red_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.start_red = None
        self.difference = None
        assert 0 <= red_val <= 1
        self.red_val = red_val
        self.should_call_pre_tick = True

    def pre_tick(self):
        self.start_red = self.target.get_red_fill()
        self.difference = self.red_val - self.start_red

    def tick(self):
        self.target.set_red_fill(
            self.target.get_red_fill() + self.difference / self.total_frames * self.rate_func(self.current_frame,
                                                                                              self.total_frames))
        return self.target


class ChangeGreen(Mutator):
    def __init__(self, target: Entity, green_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.difference = None
        self.start_green = None
        assert 0 <= green_val <= 1
        self.green_val = green_val
        self.should_call_pre_tick = True

    def pre_tick(self):
        self.start_green = self.target.get_green()
        self.difference = self.green_val - self.start_green

    def tick(self):
        self.target.set_green(
            self.target.get_green() + self.difference / self.total_frames * self.rate_func(self.current_frame,
                                                                                           self.total_frames))
        return self.target


class ChangeGreenFill(Mutator):
    def __init__(self, target: Entity, green_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.difference = None
        self.start_green = None
        assert 0 <= green_val <= 1
        self.green_val = green_val
        self.should_call_pre_tick = True

    def pre_tick(self):
        self.start_green = self.target.get_green_fill()
        self.difference = self.green_val - self.start_green

    def tick(self):
        self.target.set_green_fill(
            self.target.get_green_fill() + self.difference / self.total_frames * self.rate_func(self.current_frame,
                                                                                                self.total_frames))
        return self.target


class ChangeBlue(Mutator):
    def __init__(self, target: Entity, blue_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.difference = None
        self.start_blue = None
        assert 0 <= blue_val <= 1
        self.blue_val = blue_val
        self.should_call_pre_tick = True

    def pre_tick(self):
        self.start_blue = self.target.get_blue()
        self.difference = self.blue_val - self.start_blue

    def tick(self):
        self.target.set_blue(
            self.target.get_blue() + self.difference / self.total_frames * self.rate_func(self.current_frame,
                                                                                          self.total_frames))
        return self.target


class ChangeBlueFill(Mutator):
    def __init__(self, target: Entity, blue_val: float, start: TimeStamp, end: TimeStamp, rate_func=constant):
        super().__init__(target, start, end, rate_func)
        self.difference = None
        self.start_blue = None
        assert 0 <= blue_val <= 1
        self.blue_val = blue_val
        self.should_call_pre_tick = True

    def pre_tick(self):
        self.start_blue = self.target.get_blue_fill()
        self.difference = self.blue_val - self.start_blue

    def tick(self):
        self.target.set_blue_fill(
            self.target.get_blue_fill() + self.difference / self.total_frames * self.rate_func(self.current_frame,
                                                                                               self.total_frames))
        return self.target
