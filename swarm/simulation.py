""" Run the simulation """
import logging
import matplotlib.pyplot as plt
from typing import List

from .world import World
from .swarm import Swarm
from .recording import DummyRecorder


class SimulationResult(object):

    """ Contains the results of the simulations """

    def __init__(self):
        self._turns = 0
        self._nodes = 0
        self._discovered = []

    @property
    def turns(self) -> int:
        """ The number of turns used to finish the simulation """
        return self._turns

    @turns.setter
    def turns(self, value: int):
        """ Set the turns  """
        self._turns = value

    @property
    def discovered(self) -> List[int]:
        """ A list over the how many new nodes visists each time """
        return self._discovered

    def discovered_append(self, value):
        """ Append value to list """
        self._discovered.append(value)

    @property
    def nodes(self) -> int:
        """ The number of nodes in the world """
        return self._nodes

    @nodes.setter
    def nodes(self, value: int):
        """ The number of nodes in the world """
        self._nodes = value


class Simulator(object):

    """ The Simulator"""

    def __init__(self, world: World, display=True, speed=-1,
                 recording=DummyRecorder()):
        """ Create the simulator

        :world: TODO
        :display: TODO
        :speed:
        :recording: Record the process to the file

        """
        self._world = world
        self._display = display
        self._speed = speed
        self._turns = -1
        self._recorder = recording

    def start(self, swarm: Swarm) -> SimulationResult:
        """ Start the simulating

        :swarm: The swarm to use

        """
        logging.info("Getting the initialize position of the swarm agents")
        self._agents_positions, count_position = swarm.get_positions()

        self._result = SimulationResult()

        for p, l in zip(self._agents_positions, count_position):
            self._world.update_value(p, "agents", l)

        logging.info("Starting the simulation")

        self._main_loop(swarm)

        self._result.turns = self._turns
        self._result.nodes = self._world.size()
        return self._result

    def stop(self) -> bool:
        """ Stop the simulating (stop creteria)
        :returns: If stop creteria is reached

        """
        size = self._world.size()
        logging.debug(f"Explorated nodes: {self._explorated}, Total number of nodes: {size}")
        return not self._explorated < size - 1

    def display(self):
        """ Show the world """
        if self._display:
            plt.clf()
            plt.title(f"Turn: {self._turns}, Visisted nodes: {self._explorated}")
            self._world.view(False)
            plt.draw()
            self._recorder.record(plt.gcf())

    def sleep(self):
        """ Sleep for a time step """
        if self._speed > -1:
            plt.pause(self._speed)

    def _main_loop(self, swarm: Swarm) -> None:
        """ The main loop of the simulator

            THIS FUNCTION IS ONLY MEANT TO BE CALLED BY START

        :swarm: The swarm

        """
        self._turns = 0
        self._explorated = 0

        while not self.stop():
            logging.debug(f"Turn {self._turns} is now running")
            self.display()
            self._turn(swarm)
            self._turns += 1
            self.sleep()
        
        logging.info("Simulation is done")
        if self._display:
            self.display()
            plt.show()

    def _turn(self, swarm: Swarm):
        """ A simulation turn

            THIS FUNCTION IS ONLY MEANT TO BE CALLED BY _MAIN_LOOP

        :swarm: The swarm to use

        """
        logging.debug("Reseting the agents position in the  map")
        for p in self._agents_positions:
            self._world.update_value(p, "agents", 0)

        new_explorated = swarm.move_all(self._world)
        self._explorated += new_explorated

        self._result.discovered_append(new_explorated)

        logging.debug("Adding the agents new position to the map")

        self._agents_positions, count_position = swarm.get_positions()

        for p, l in zip(self._agents_positions, count_position):
            self._world.update_value(p, "agents", l)
