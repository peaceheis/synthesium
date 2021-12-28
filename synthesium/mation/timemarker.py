class TimeMarker: 
    def __init__(self, minute=0, second=0, frame=0): 
        self.minute = minute
        self.second = second
        self.frame = frame

    def time_as_tuple(self): 
        return (self.minute, self.second, self.frame)

    def frame(self, fps): 
        return self.minute * 60 * fps + self.second * fps + self.frame