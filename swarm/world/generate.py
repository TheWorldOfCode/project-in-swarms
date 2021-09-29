""" Generate a world """
from typing import Tuple
import networkx as nx
import random as rnd
import logging

from .world import World
from .color import START


class WorldGenerator(object):

    """ Autogenerating worlds"""

    def __init__(self, nodes: Tuple[int, int],
                 edge_multiplier: float, weight_range: Tuple[int, int],
                 seed=rnd.seed()):
        """ Create a generator

        :nodes: The range of the possible nodes
        :edge_multiplier: The maximum number of edges is calculated by nodes * edge_multiplier
        :weight_range: The range of the weight for the edges
        :seed: The seed for the random generator

        """
        assert nodes[0] > 0, "The mini number of nodes must be a positive integer"
        assert nodes[0] < nodes[1], "The minimum number must be be smaller or equal to the maximum number of nodes"
        assert edge_multiplier > 0, "The edge multiplier must be a positive number"
        assert type(weight_range) == tuple and len(weight_range) == 2, "The weight range is either not a tuple of doesn't have the correct size"
        assert weight_range[0] <= weight_range[1], "The first integer in the range must be the smallest"

        self._min_node, self._max_node = nodes
        self._edge_multiplier = edge_multiplier
        self._seed = seed
        self._min_weight, self._max_weight = weight_range
        self.reset()

    def reset(self) -> None:
        """ Reset the generator to begining

        """
        rnd.seed(self._seed)

    def generate(self) -> World:
        """ Generate a world
        :returns: TODO

        """
        logging.info("Generating world")

        nodes = rnd.randrange(self._min_node, self._max_node)
        edge_count = rnd.randint(nodes, int(nodes * self._edge_multiplier))
        seed = rnd.randint(0, 10000000000)

        logging.info(f'''World generator settings: Seed: {self._seed} Number nodes: {nodes} Edge count: {edge_count} Weight seed: {seed} ''')

        logging.info("Generating complete world")
        world: nx.Graph = nx.gnm_random_graph(nodes, edge_count)

        logging.info("Connecting unconnected nodes")
        for i in nx.isolates(world):
            selected = i
            while True:
                selected = rnd.randint(0, nodes-1)
                if selected != i and len(list(nx.neighbors(world, selected))) != 0:
                    world.add_edge(i, selected)
                    break

        world.nodes[0]['color'] = START
        logging.info("Adding randoms weights to edges")

        state = rnd.getstate()
        rnd.seed(seed)
        labels = {}
        for edge in nx.edges(world):
            i, j = edge
            weight = rnd.randint(self._min_weight, self._max_weight)
            world[i][j]["weight"] = weight
            labels[edge] = weight

        rnd.setstate(state)
        logging.info("World generated")

        return World(world, labels)
