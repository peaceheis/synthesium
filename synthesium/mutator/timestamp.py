from synthesium.utils.defaults import DEFAULT_FPS

FPS = DEFAULT_FPS


class TimeStamp:
    def __init__(self, minute: int = 0, second: int = 0, frame: int = 0):
        self.minute = minute
        self.second = second
        self.frame = frame

    def set(self, **kwargs):
        for attr in kwargs.keys():
            self.__setattr__(attr, kwargs[attr])

    def __repr__(self):
        return f"synthesium.mutator.timestamp.TimeStamp({self.minute}, {self.second}, {self.frame})"

    def __str__(self):
        return f"TimeStamp with minute {self.minute}, second {self.second}, frame {self.frame}"

    def increment(self):
        self.frame += 1
        if self.frame >= FPS:
            self.frame = 0
            self.second += 1

        if self.second > 59:
            self.second = 0
            self.minute += 1

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
        return self.minute, self.second, self.frame

    def time_as_int(self, fps=FPS):
        return self.minute * 60 * FPS + self.second * FPS + self.frame

    def __gt__(self, marker: "TimeStamp"):
        if self.minute > marker.minute:
            return True
        elif self.minute == marker.minute:
            if self.second > marker.second:
                return True
            elif self.second == marker.second:
                if self.frame > marker.frame:
                    return True
        return False

    def is_after(self, marker: "TimeStamp"):
        return self.__gt__(marker)

    def __lt__(self, marker: "TimeStamp"):
        if self.minute < marker.minute:
            return True
        elif self.minute == marker.minute:
            if self.second < marker.second:
                return True
            elif self.second == marker.second:
                if self.frame < marker.frame:
                    return True
        return False

    def is_before(self, marker: "TimeStamp"):
        return self.__lt__(marker)

    def __eq__(self, marker: "TimeStamp"):
        return (
            self.minute == marker.minute
            and self.second == marker.second
            and self.frame == marker.frame
        )

    def is_equal_to(self, marker: "TimeStamp"):
        return self.__eq__(marker)

    def __ge__(self, marker: "TimeStamp"):
        return self.__gt__(marker) or self.__eq__(marker)

    def is_equal_to_or_after(self, marker: "TimeStamp"):
        return self.__ge__(marker)

    def __le__(self, marker: "TimeStamp"):
        return self.__lt__(marker) or self.__eq__(marker)

    def is_equal_to_or_before(self, marker: "TimeStamp"):
        return self.__le__(marker)
