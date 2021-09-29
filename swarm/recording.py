""" Recording the simulation """
from tempfile import TemporaryDirectory
import logging
import os


class DummyRecorder(object):

    """ This is a dummy recorder"""

    def __init__(self):
        pass

    def record(self, fig):
        pass


class VideoRecorder(object):

    """ Video recording the simulation """

    def __init__(self, fps):
        """ Create the Video Recorder

            :fps: frames pr second
        """
        self._temp_dir = TemporaryDirectory()
        self._temp = self._temp_dir.name
        logging.debug(f"Recording temperary directory: {self._temp}")
        self._frame_id = 0
        self._fps = fps

    def record(self, fig) -> None:
        """ Perform a recording of a matplotlib figure

        """
        logging.debug(f"Recording frame {self._frame_id}")
        fig.savefig(f"{self._temp}/frame_{self._frame_id}")
        self._frame_id += 1

    def save(self, filename):
        """ Save the video

        :filename: The filename of the video

        """
        os.system(f"ffmpeg -r {self._fps} -i {self._temp}/frame_%01d.png -vcodec mpeg4 -y {filename}")
