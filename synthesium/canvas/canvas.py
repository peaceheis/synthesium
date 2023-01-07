import os
import os.path
import subprocess
from abc import ABC

import cairo
import numpy as np

from synthesium.entity.entity import Entity
from synthesium.mutator import timestamp
from synthesium.mutator.timestamp import TimeStamp
from synthesium.utils import defaults
from synthesium.utils.defaults import DEFAULT_FPS, FFMPEG_BIN


class Canvas(ABC):
    """The canvas acts as the entry point between the user and Synthesium. The user creates a class that inherits
    from Canvas, and overrides construct. They then must instantiate their custom class, and
    run save("end_directory"), which returns the finished video. All the rendering gets done after that method is called,
    breaking EntityGroups down to Primitives, which cairo then draws.
    In addition, animation goes on here, by calling tick() on every active Mutator.
    """

    def __init__(
        self,
        /,
        path: str,
        width: int,
        height: int,
        fps=DEFAULT_FPS,
        background_frame=None,
    ) -> None:
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
        self.construct()
        self.end = max(entity.end for entity in self.entities)
        self.save(path)

    def get_dimensions(self):
        return self.width, self.height

    def launch_writing_subprocess(self, end_dir):
        if not os.path.exists(
            os.path.split(end_dir)[0]
        ):  # TODO: create directory ourself!
            raise Exception(
                f"directory {end_dir} provided to Canvas {self.__class__.__name__} does not exist."
            )

        command = [
            FFMPEG_BIN,
            "-y",  # overwrite output file if it exists
            "-f",
            "rawvideo",
            "-s",
            str(self.width) + "x" + str(self.height),  # size of one frame
            "-pix_fmt",
            "rgba",
            "-r",
            str(self.fps),  # frames per second
            "-i",
            "-",  # The input comes from a pipe
            "-an",  # Tells FFMPEG not to expect any audio
            "-loglevel",
            "error",
            "-vcodec",
            "libx264",
            "-pix_fmt",
            "yuv420p",
        ]

        command += [end_dir]
        return subprocess.Popen(command, stdin=subprocess.PIPE)
        # credit to Manim (https://github.com/3b1b/manim).
        # I adapted this code from scene_file_writer.py, in the cairo-backend branch. Brilliant code there.

    def save(self, end_dir: str):
        print(f"Starting Write of {self.__class__.__name__}")
        self.process = self.launch_writing_subprocess(end_dir)

        arr = np.zeros(self.width * self.height, np.uint32)
        arr = arr.reshape(self.width, self.height)

        while self.current_frame < self.end:
            print(f"Processing frame {self.current_frame}")
            self.current_frame.increment()
            for entity in self.entities:
                if not entity.active_at(self.current_frame):
                    continue

                start_x, start_y = entity.get_top_left_coords()
                x_size, y_size = entity.get_size()
                render = entity.render(self.current_frame, fps=self.fps)

                for x, arr_x in enumerate(range(x_size)):
                    for y, arr_y in enumerate(range(y_size)):
                        arr[x + start_x, y + start_y] = render[x, y]

            self.process.stdin.write(arr.tobytes())

        self.process.stdin.close()
        self.process.wait()
        self.process.terminate()

    def construct(self):
        """Construct() lies at the heart of Synthesium. All mutators should be played in self.construct(), which the
        internal pipeline looks for when creating an animation. This idea from this comes from 3b1b's Manim. Check it out at https://github.com/3b1b/manim"""
