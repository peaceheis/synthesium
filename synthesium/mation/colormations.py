from synthesium.matable.matable import Matable
from synthesium.mation.mation import Mation
from synthesium.mation.timestamp import TimeStamp
from synthesium.utils.imports import *

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