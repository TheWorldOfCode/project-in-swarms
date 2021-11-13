""" Swarm """
from typing import Callable as Func, List, Tuple
from statistics import mean, stdev
from swarm.world import color


class SwarmSummary(object):

    """
        This is a quick summary of the swarm.
        This would provide the following information:
            - Lowest traveling distance for all agents.
            - Mean traveling distance for all agents.
            - Std. varaince of the traveling distance.
            - Highest traveling distance.

    """

    def __init__(self, raw, lowest: float, mean: float, std: float, highest: float):
        """

        :raw: The raw data
        :lowest: The lowest traveling distance
        :mean: The mean traveling distance
        :std: The std varaince of traveling distance
        :higest: The highest traveling distance

        """
        self._raw = raw
        self._lowest = lowest
        self._mean = mean
        self._std = std
        self._highest = highest

    @property
    def lowest(self) -> float:
        """ Get the lowest """
        return self._lowest

    @property
    def mean(self) -> float:
        """ Get the mean """
        return self._mean

    @property
    def std(self) -> float:
        """ Get the variance """
        return self._std

    @property
    def highest(self) -> float:
        """ Get the highest """
        return self._highest

    def __str__(self):
        return f"Swarm summary\n\tLowest traveling distance {self.lowest}\n\tMean traveling distance {self.mean} (±{self.std})\n\tHighest traveling distance {self.highest}"


class Swarm(object):

    """ This a wrapper for the all agents """

    def __init__(self, agent_generators: List[Tuple[int, Func]]):
        """ Create the swarm """
        self._generator = agent_generators

        self._agents = []
        self._positions = {}

        self.create_swarm()

    def create_swarm(self) -> None:
        """ Create the swarm according to the generators """

        self._agents.clear()

        for amount, gen in self._generator:
            for i in range(amount):
                agent = gen()
                #                assert issubclass(agent, AgentInterface), "The agent must be a subclass of swarm.agent.AgentInterface"
                self._agents.append(agent)

        self._get_position()

    def move_all(self, world):
        """ Move all agents in the swarm

        :world: The world
        :returns: The amount of new explorated nodes

        """
        positions = {}
        agent_movement = []

        for agent in self._agents:
            old_pos = agent.position
            pos = agent.move(world, agent_movement)
            agent_movement.append([old_pos, pos])
            positions.setdefault(str(pos), 0)
            positions[str(pos)] += 1

        new_explorated = 0
        for k in positions.keys():
            new_explorated += int(world.explore(k))

        self._positions.clear()
        self._positions = positions

        return new_explorated

    def set_positions(self, position: int) -> None:
        """ Set the same position for all agents in swarm

        :position: The node id

        """
        for agent in self._agents:
            agent.position = position

        self._positions.clear()
        self._positions[str(position)] = len(self._agents)

    def get_positions(self) -> Tuple[List[int], List[int]]:
        """ Get the position of the swarm
        :returns: The position and the number of agent in different positions

        """
        return self._positions.keys(), self._positions.values()

    def summary(self) -> SwarmSummary:
        """ Get the summary of the swarm

        :returns: The summary

        """
        traveling_distance = []
        for a in self._agents:
            traveling_distance.append(a.traveled_distance)

        low = min(traveling_distance)
        m = mean(traveling_distance)
        s = stdev(traveling_distance)
        high = max(traveling_distance)

        return SwarmSummary(traveling_distance, low, m, s, high)

    def _get_position(self) -> None:
        """ Get the position from the agent
        (this is only used for getting the initialize position)
        """
        self._positions.clear()

        for agent in self._agents:
            pos = agent.position

            self._positions.setdefault(str(pos), 0)
            self._positions[str(pos)] += 1
