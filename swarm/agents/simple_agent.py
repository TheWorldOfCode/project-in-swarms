""" A simple agent only according number of other agents """
from . AgentInterface import AgentInterface

import random as rnd
from typing import Callable


class SimpleAgent(AgentInterface):

    """ A random walk agent """

    def move(self, world) -> int:
        """ Move the agent

        :world: The world
        :returns: The new node it would move to

        """
        canndidates = world.connected(self.position)
        new_position = rnd.choice(canndidates)

        self.traveled_distance += world.cost(self.position, new_position)
        self.position = new_position

        return self._position


def simple_agent_generator() -> Callable:
    """ Create a simple agent generator

    :returns: A generator function

    """

    def generator():
        return SimpleAgent(None, rnd.randint(0, 10))

    return generator
