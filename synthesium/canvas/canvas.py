import os
import os.path
import subprocess

import cairo
import numpy
from cairo import ImageSurface

from synthesium.entity.entitygroup import EntityGroup
from synthesium.entity.primitives import Line, Arc, Curve
from synthesium.mutator.mutator import Mutator
from synthesium.mutator.mutatorgroup import MutatorGroup
from synthesium.utils.defaults import DEFAULT_FPS, FFMPEG_BIN, DEFAULT_FRAME_WIDTH, DEFAULT_FRAME_HEIGHT


class Canvas:
    """The canvas acts as the entry point between the user and Synthesium. The user creates a class that inherits
    from Canvas, and overrides construct. They then must instantiate their custom class, and
    run save("end_directory"), which returns the finished video. All the rendering gets done after that method is called,
    breaking EntityGroups down to Primitives, which cairo then draws.
    In addition, animation goes on here, by calling tick() on every active Mutator.
    """

    def __init__(self, /,
                 background_color: tuple = (0, 0, 0, 1),
                 fps: int = DEFAULT_FPS,
                 canvas_size: tuple = (DEFAULT_FRAME_WIDTH, DEFAULT_FRAME_HEIGHT),
                 frame_size: object = (DEFAULT_FRAME_WIDTH, DEFAULT_FRAME_HEIGHT)) -> None:
        # TODO, make a better default frame size
        self.pipe = None
        self.mutators = []
        self.background_color = background_color
        self.fps = fps
        self.width, self.height = canvas_size  # canvas size is the size of the canvas in which everything will be
        # drawn...
        self.frame_width, self.frame_height = frame_size  # ...frame size is the size of the output video. this
        # allows for things like panning cameras. (which has not yet been implemented.)
        self.count = 0

        # cairo things
        self.surface = ImageSurface(cairo.Format.ARGB32, self.width, self.height)
        self.ctx = cairo.Context(self.surface)
        self.initialize_surface()

    def get_dimensions(self):
        return self.width, self.height  # TODO work on capturing

    def initialize_surface(self):
        """initialize background color"""
        self.ctx.move_to(0, 0)
        self.ctx.set_source_rgba(*reversed(self.background_color[0:3]), self.background_color[3])
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

    def add(self, *mutators):
        """calling self.add(mutator) doesn't do much besides add it to the list of mutators to be processed. The heavy lifting is done when
        Canvas.write() is called, outside the class definition."""
        self.count += 1
        for mutator in mutators:
            mutator.set_fps(self.fps)
            self.mutators.append(mutator)

    # auxiliary functions to save()

    def sort_mutatorlist(self):
        """Sorts the mutatorlist by start frame. It assumes that the Mutators have been add()ed, and therefore have
           had their fps set."""
        return sorted(self.mutators, key=Mutator.get_start_as_int)

    def merge_mutators(self):
        """Take all the mutators in a list and compress them into a list of MutatorGroup to remove any overlap between
           mutators. This is used with Canvas to ensure only one Mutator (or MutatorGroup) has to be handled at a time."""
        return [MutatorGroup(*self.mutators, fps=self.fps)]  # TODO write a functioning mutator merging method

    def open_pipe_for_rendering(self, end_dir):
        if not os.path.exists(os.path.split(end_dir)[0]):
            raise Exception(f"directory {end_dir} provided to Canvas {self.__class__.__name__} does not exist.")

        command = [
            FFMPEG_BIN,
            '-y',  # overwrite output file if it exists
            '-f', 'rawvideo',
            '-s', str(self.frame_width) + 'x' + str(self.frame_height),  # size of one frame
            '-pix_fmt', 'rgba',
            '-r', str(self.fps),  # frames per second
            '-i', '-',  # The input comes from a pipe
            '-an',  # Tells FFMPEG not to expect any audio
            '-loglevel', 'error',
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
        ]

        command += [end_dir]  # TODO, implement partial movie files à la Manim.
        return subprocess.Popen(command, stdin=subprocess.PIPE)
        # credit to Manim (https://github.com/3b1b/manim). 
        # I adapted this code from scene_file_writer.py, in the cairo-backend branch. Brilliant code there.

    def draw_line(self, line: Line):
        self.ctx.set_source_rgba(*reversed(line.config["color"][0:3]),
                                 line.config["color"][3])  # TODO, implement full customization for context
        self.ctx.set_line_width(line.config["line_width"])
        self.ctx.new_sub_path()
        self.ctx.move_to(*line.get_point1().as_tuple())
        self.ctx.line_to(*line.get_point2().as_tuple())
        self.ctx.stroke_preserve()
        self.ctx.set_source_rgba(*reversed(line.config["fill_color"][0:3]), line.config["fill_color"][3])
        self.ctx.fill()  # 5b

    def draw_arc(self, arc: Arc):
        self.ctx.set_source_rgba(*reversed(arc.config["color"][0:3]), arc.config["color"][3])
        self.ctx.set_line_width(arc.config["line_width"])
        self.ctx.new_sub_path()
        if arc.negative:
            self.ctx.arc_negative(*arc.get_center().as_tuple(), arc.get_radius(), arc.get_angle1(), arc.get_angle2())
        else:
            self.ctx.arc(*arc.get_center().as_tuple(), arc.get_radius(), arc.get_angle1(), arc.get_angle2())
        self.ctx.stroke_preserve()
        self.ctx.set_source_rgba(*reversed(arc.config["fill_color"][0:3]), arc.config["fill_color"][3])
        self.ctx.fill()  # 5c

    def draw_curve(self, curve: Curve):
        self.ctx.set_source_rgba(*reversed(curve.config["color"][0:3]), curve.config["color"][3])
        self.ctx.set_line_width(curve.config["line_width"])
        self.ctx.new_sub_path()
        self.ctx.move_to(*curve.get_points()[0].as_tuple())
        self.ctx.curve_to(*curve.get_points()[0].as_tuple(), *curve.get_points()[1].as_tuple(),
                          *curve.get_points()[2].as_tuple())
        self.ctx.stroke_preserve()
        self.ctx.set_source_rgba(*reversed(curve.config["fill_color"][0:3]), curve.config["fill_color"][3])
        self.ctx.fill()  # 5d

    def draw_entity_group(self, mgroup: EntityGroup):
        to_be_drawn: list = mgroup.get_entities_by_type(Line)
        for line in to_be_drawn:
            self.draw_line(line)

        to_be_drawn: list = mgroup.get_entities_by_type(Arc)
        for arc in to_be_drawn:
            self.draw_arc(arc)

        to_be_drawn: list = mgroup.get_entities_by_type(Curve)
        for curve in to_be_drawn:
            self.draw_curve(curve)

    def draw_vector_entities(self, entity):
        # EntityGroup handling
        if isinstance(entity, EntityGroup):
            self.draw_entity_group(entity)  # 5b
            return True

        elif isinstance(entity, Line):
            self.draw_line(entity)  # 5c
            return True

        elif isinstance(entity, Arc):
            self.draw_arc(entity)  # 5d
            return True

        elif isinstance(entity, Curve):
            self.draw_curve(entity)  # 5e
            return True

        else:
            return False

    def save(self, end_dir: str):
        """This is where all the rendering work gets done. The steps are as follows:
                1. The mutator list is constructed (by calling the user-defined construct()), and sorted by start frame,
                2. A compressed list where any overlapping mutators are made into a MutatorGroup is generated,
                3. After verification of the end directory, a pipe is opened to ffmpeg to string together all the frames.
                5. The animation then gets rendered via loop: 
                    5a. Make the animation progress 1 frame, and get all the entities to be drawn in that frame.
                    5b. Break them down, and render the primitives Line, Arc, and Curve.
                6. The video is written."""

        if len(self.mutators) == 0:
            raise Exception("No mutators were added!")
        self.mutators = self.sort_mutatorlist()  # 1
        self.mutators = self.merge_mutators()  # 2
        self.pipe = self.open_pipe_for_rendering(end_dir)  # 3

        for mutator in self.mutators:
            print(f"Processing mutator {mutator}")
            if mutator.should_call_pre_tick:
                mutator.pre_tick()
            for _ in mutator.get_range_of_frames():  # 5
                print(f"processing frame {mutator.current_frame}")
                entity = mutator.tick()  # 5a.
                valid = self.draw_vector_entities(entity)  # 5b
                if not valid:
                    raise Exception(f"Entity {entity} returned by mutator {mutator} not drawable.")

                width, height = self.get_dimensions()
                buf = self.surface.get_data()
                data = numpy.ndarray(shape=(height, width),
                                     dtype=numpy.uint32,
                                     buffer=buf)
                self.pipe.stdin.write(data.tobytes())  # 5g.

                self.initialize_surface()

        self.pipe.stdin.close()
        self.pipe.wait()
        self.pipe.terminate()  # 6

    def write(self, enddir: str):  # funny how the most involved method is the shortest.
        self.construct()
        self.save(enddir)

    def construct(self):
        """Construct() lies at the heart of Synthesium. All mutators should be played in self.construct(), which the 
        internal pipeline looks for when creating an animation. This idea from this comes from 3b1b's Manim. Check it out at https://github.com/3b1b/manim"""
