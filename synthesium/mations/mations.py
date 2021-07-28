from synthesium.mations.mation import Mation
from synthesium.matables.matable import Matable

#some predefined Mations
class Show(Mation): 
    def __init__(self, target: Matable, start_second: int, start_frame, end_second, end_frame, rate_func): 
        super().__init__(target, start_second, start_frame, end_second, end_frame, rate_func)

    def tick(self): 
        return self.target

class Move(Mation):
    def __init__(self, target: Matable, amount: tuple, start_second: int, start_frame, end_second, end_frame, rate_func):
        super().__init__(target, start_second, start_frame, end_second, end_frame, rate_func)
        self.amount = amount

    def tick(self): 
        single_frame_amount = [amt/self.total_frames for amt in self.amount]
        adjusted_frame_amount = [amt * self.rate_func(self.current_frame, self.total_frames) for amt in single_frame_amount]
        return self.target.shift(tuple(adjusted_frame_amount))

    def __repr__(self): 
        return f"Mation({self.target}, {self.amount}, {self.start_second}, {self.start_frame}, {self.end_second}, {self.end_frame}"
