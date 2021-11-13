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


class DummyDataRecorder(object):

    """ This is a dummy data recorder"""

    def __init__(self, filename="results.yaml"):
        """ Create the recorder 
            :filename: The file to save to 
        """
        self._filename = filename
        self._data_functions = []

    def save(self, sim, swarm):
        """ Save the results of simulation to file
            :sim: The simulation
            :swarm: The swarm
        """

        if len(self._data_functions) != 0:
            with open(self._filename, "w") as f:
                for func in self._data_functions:
                    func(sim, swarm, f)


class BasicDataRecorder(DummyDataRecorder):

    """ Saving the basic information from the simulation"""

    def __init__(self, filename="result.yaml"):
        """ Create the recorder

        :filename: The file to save to

        """
        DummyDataRecorder.__init__(self, filename)
        self._data_functions.append(self.summary)

    def summary(self, sim, swarm, f):
        """ Save the summary

        :sim: The simulation
        :swarm: The swarm
        :f: The file

        """
        sim_results = sim.get_results()
        f.write(f"seed: {sim_results.seed}\n")
        f.write(f"nodes: {sim_results.nodes}\n")
        f.write(f"turns: {sim_results.turns}\n")
        f.write(f"discovered: {sim_results.discovered}\n")

        swarm_summary = swarm.summary()
        f.write(f"swarm_lowest_travel_distance: {swarm_summary.lowest}\n")
        f.write(f"swarm_mean_travel_distance: {swarm_summary.mean}\n")
        f.write(f"swarm_std_travel_distance: {swarm_summary.std}\n")
        f.write(f"swarm_highest_travel_distance: {swarm_summary.highest}\n")
        f.write(f"raw_travel_distance: {swarm_summary._raw}\n")


class AgentDataRecorder(BasicDataRecorder):

    """ Recorder information about the agents """

    def __init__(self, filename="result.yaml"):
        """ Create the recorder

        :filename: The file to save to

        """
        BasicDataRecorder.__init__(self, filename)
        self._data_functions.append(self.agent_history)
        logging.warn("AgentDataRecorder requires that agents has enable there history for workning")

    def agent_history(self, sim, swarm, f):
        """ Save the movement history of the agent

        :sim: The simulation
        :swarm: The swarm
        :f: The file

        """
        f.write("agents_history: [\n")

        for agent in swarm._agents:
            f.write(f"{agent._history},\n")

        f.write("]\n")

        f.write("agents_record: [\n")

        for agent in swarm._agents:
            f.write(f"{agent._record},\n")

        f.write("]\n")



DATA_RECORDER_LIST = [DummyDataRecorder.__name__, BasicDataRecorder.__name__, AgentDataRecorder.__name__]
