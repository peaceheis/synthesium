class TimeMarker: 
    def __init__(self, minute:int=0, second:int=0, frame:int=0): 
        self.minute = minute
        self.second = second
        self.frame = frame

    def set(self, **kwargs): 
        for attr in kwargs.keys(): 
            self.__setattr__(attr, kwargs[attr])

    def get_minute(self): 
        return self.minute

    def set_minute(self, minute): 
        assert type(minute) == int
        self.minute = minute
        return self

    def get_second(self): 
        return self.second
    
    def set_second(self, second: int): 
        assert type(second) == int
        self.second = second
        return self

    def get_frame(self): 
        return self.frame

    def set_frame(self, frame: int): 
        assert type(frame) == int
        self.frame = frame
        return self

    def time_as_tuple(self): 
        return (self.minute, self.second, self.frame)

    def time_as_int(self, fps): 
        return self.minute * 60 * fps + self.second * fps + self.frame

    def __gt__(self, marker: "TimeMarker"): 
        if self.minute > marker.minute: 
            return True
        elif self.minute == marker.minute: 
            if self.second > marker.second: 
                return True
            elif self.second == marker.second: 
                if self.frame > marker.frame: 
                    return True
        return False

    def is_after(self, marker: "TimeMarker"): 
        return self.__gt__(marker)

    def __lt__(self, marker: "TimeMarker"): 
        if self.minute < marker.minute: 
            return True
        elif self.minute == marker.minute: 
            if self.second < marker.second: 
                return True
            elif self.second == marker.second: 
                if self.frame < marker.frame: 
                    return True
        return False

    def is_before(self, marker: "TimeMarker"): 
        return self.__lt__(marker)

    def __eq__(self, marker: "TimeMarker"): 
        return self.minute == marker.minute and self.second == marker.second and self.frame == marker.frame

    def is_equal_to(self, marker: "TimeMarker"): 
        return self.__eq__(marker)

    def __ge__(self, marker: "TimeMarker"): 
        return self.__gt__(marker) or self.__eq__(marker)

    def is_equal_to_or_after(self, marker: "TimeMarker"): 
        return self.__ge__(marker)

    def __le__(self, marker: "TimeMarker"): 
        return self.__lt__(marker) or self.__eq__(marker)

    def is_equal_to_or_before(self, marker: "TimeMarker"): 
        return self.__le__(self, marker)
        
    def __str__(self): 
        return f"{self.__class__.__name__} at min {self.minute}, sec {self.second}, and frame {self.frame}"

