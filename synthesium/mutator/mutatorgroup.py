from synthesium.entity.entity import Entity
from synthesium.entity.entitygroup import EntityGroup
from synthesium.mutator.mutator import Mutator
from synthesium.mutator.timestamp import TimeStamp


class MutatorGroup(Mutator):
    """a Mutator composed of mutators, used internally with Canvas so that it only has to process one Mutator at a time, which simplifies a lot of logic."""

    def __init__(self, target: Entity, start: TimeStamp, end: TimeStamp, *mutators, fps=None):
        super().__init__(target, start, end)
        self.should_call_pre_tick = False
        self.mutators = [mutator for mutator in mutators]
        self.pre_tickers = [mutator for mutator in mutators if mutator.should_call_pre_tick]
        if len(self.pre_tickers) > 0:
            self.should_call_pre_tick = True

        self.current_frame = 0
        if len(mutators) > 0:  # to prevent an empty MutatorGroup to run into issues with bound updating
            self.update_bounds()
        else:
            self.start = TimeStamp(0, 0, 0)
            self.end = TimeStamp(0, 0, 0)
        self.fps = fps
        if self.fps is not None:
            self.total_frames = self.end.time_as_int(self.fps) - self.start.time_as_int(self.fps) + 1
        else:
            self.total_frames = None

    def update_bounds(self):
        start = sorted(self.mutators, key=Mutator.get_start)[0].get_start()
        end = sorted(self.mutators, key=Mutator.get_end, reverse=True)[0].get_end()
        if not end > start:
            raise Exception("Mutator's end comes before start")
        self.start = start
        self.end = end

    def pre_tick(self):
        for mutator in self.pre_tickers:
            mutator.pre_tick()

    def tick(self):
        self.current_frame += 1
        return EntityGroup(*[mutator.tick() for mutator in self.mutators if mutator.is_active_at_frame(
            self.current_frame)])  # returns  an EntityGroup of returned mutators for each ticked mutator

    def __str__(self):
        string = f"MutatorGroup of type {self.__class__.__name__}, composed of"
        for mutator in self.mutators:
            string += f"\n\t Mutator of type {mutator.__class__.__name__} running from {mutator.start} to {mutator.end}"
        return string

    def add(self, *mutators):
        assert (
            all([isinstance(mutator, Mutator) for mutator in mutators]))  # ensure all the arguments given are mutators
        self.mutators.append(*mutators)
        self.update_bounds()

    def remove_mation_by_index(self, index):  # in case a Mutator hasn't been bound to a variable.
        del self.mutators[index]  # if there's an IndexError, Python will let the user know.

    def remove(self, *mutators):
        """Remove mutators from the mutator list"""
        self.mutators = [mutator for mutator in self.mutators if
                         mutator not in mutators]  # regenerate mutatorlist without the mutators in the list.
        self.update_bounds()

    def set_fps(self, fps):
        super().set_fps(fps)
        for mutator in self.mutators:
            mutator.set_fps(fps)

    def set_start(self, start: TimeStamp):
        raise Exception("Setting start and end is not allowed with mutators of type MutatorGroup.")

    def set_end(self, end: TimeStamp):
        raise Exception("Setting start and end is not allowed with mutators of type MutatorGroup.")

    def get_mations(self):
        return self.mutators

    def __repr__(self) -> str:
        return self.__str__()  # TODO create MutatorGroup repr


class SameTargetGroup(MutatorGroup):
    """For when you want multiple mutators to target the same Entity."""

    def __init__(self, target, *mutators, fps=None):
        super().__init__(*mutators, fps=fps)
        self.target = target

    def tick(self):
        self.current_frame += 1
        for mutator in self.mutators:
            if mutator.is_active_at_frame(self.current_frame):
                mutator.tick()

        return self.target
