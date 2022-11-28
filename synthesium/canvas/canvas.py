import os
import os.path
import subprocess
import warnings

import cairo
import numpy
import numpy as np
from cairo import ImageSurface

from synthesium.entity.entity import Entity
from synthesium.mutator import timestamp
from synthesium.mutator.mutator import Mutator
from synthesium.mutator.timestamp import TimeStamp
from synthesium.utils import defaults
from synthesium.utils.defaults import DEFAULT_FPS, FFMPEG_BIN, DEFAULT_FRAME_WIDTH, DEFAULT_FRAME_HEIGHT


class Canvas:
    """The canvas acts as the entry point between the user and Synthesium. The user creates a class that inherits
    from Canvas, and overrides construct. They then must instantiate their custom class, and
    run save("end_directory"), which returns the finished video. All the rendering gets done after that method is called,
    breaking EntityGroups down to Primitives, which cairo then draws.
    In addition, animation goes on here, by calling tick() on every active Mutator.
    """

    def __init__(self, /,
                 path: str,
                 width: int,
                 height: int,
                 fps=DEFAULT_FPS,
                 background_frame = None) -> None:
        # TODO, make a better default frame size

        self.fps = fps
        self.entity_count = 0
        self.entities: list[Entity] = []
        self.width = width
        self.height = height
        self.process = None
        timestamp.FPS = fps
        self.current_frame = TimeStamp()
        self.background_frame = background_frame
        self.end = TimeStamp()
        self.construct()
        self.write(path)

    def get_dimensions(self):
        return self.width, self.height

    def launch_writing_subprocess(self, end_dir):
        if not os.path.exists(os.path.split(end_dir)[0]):
            raise Exception(f"directory {end_dir} provided to Canvas {self.__class__.__name__} does not exist.")

        command = [
            FFMPEG_BIN,
            '-y',  # overwrite output file if it exists
            '-f', 'rawvideo',
            '-s', str(self.width) + 'x' + str(self.height),  # size of one frame
            '-pix_fmt', 'rgba',
            '-r', str(self.fps),  # frames per second
            '-i', '-',  # The input comes from a pipe
            '-an',  # Tells FFMPEG not to expect any audio
            '-loglevel', 'error',
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
        ]

        command += [end_dir]
        return subprocess.Popen(command, stdin=subprocess.PIPE)
        # credit to Manim (https://github.com/3b1b/manim). 
        # I adapted this code from scene_file_writer.py, in the cairo-backend branch. Brilliant code there.

    def save(self, end_dir: str):
        self.process = self.launch_writing_subprocess(end_dir)
        arr = self.background_frame or np.zeros((self.width, self.height, defaults.DEFAULT_COLOR_DEPTH))

        while self.current_frame < self.end:
            self.current_frame.increment()
            for entity in self.entities:
                if not entity.active_at(self.current_frame):
                    continue

                start_x, start_y = entity.get_top_left_coords()
                x_size, y_size = entity.get_size()
                render = entity.render(self.current_frame, fps=self.fps)

                for x in range(start_x, start_x+x_size):
                    for y in range(start_y, start_y+y_size):
                        arr[x, y] = entity.blending_func(arr, render)

            self.process.stdin.write(arr.tobytes())


        self.process.stdin.close()
        self.process.wait()
        self.process.terminate()

    def write(self, enddir: str):  # funny how the most involved method is the shortest.
        self.construct()
        self.save(enddir)

    def construct(self):
        """Construct() lies at the heart of Synthesium. All mutators should be played in self.construct(), which the 
        internal pipeline looks for when creating an animation. This idea from this comes from 3b1b's Manim. Check it out at https://github.com/3b1b/manim"""
