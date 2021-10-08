""" A random walk agent """
from . AgentInterface import AgentInterface

import random as rnd
from typing import Callable


class RandomAgent(AgentInterface):

    """ A random walk agent """

    def move(self, world, updated_pos) -> int:
        """ Move the agent

        :world: The world
        :updated_pos: The updated position of agents already moved
        :returns: The new node it would move to

        """
        canndidates = world.connected(self.position)
        new_position = rnd.choice(canndidates)

        self.traveled_distance += world.cost(self.position, new_position)
        self.position = new_position

        return self._position


def random_agent_generator() -> Callable:
    """ Create a random agent generator

    :returns: A generator function

    """

    def generator():
        return RandomAgent(None, rnd.randint(0, 10))

    return generator
