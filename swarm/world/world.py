""" Contains the world description for the swarm """
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import logging

from .color import UNEXPLORATED, EXPLORATED, START, ClassicColor


class World(object):

    """ The world representation """

    def __init__(self, map, labels):
        """TODO: to be defined. """
        logging.debug("Initializing the world")
        self._map = map
        self._labels = labels

    def reset(self):
        """ Reset the map """
        for i in range(len(self._map.nodes)):
            self.update_value(i, "color", UNEXPLORATED)
            
    def connected(self, node: int) -> list:
        """ Get the corrected nodes to node

        :node: The node id
        :returns: list of node

        """
        return list(nx.neighbors(self._map, node))

    def explore(self, node) -> bool:
        """ Set the node as explorated

        :node: The node id
        :return: True if it was unexplorated

        """
        node = int(node)
        assert 0 <= node <= nx.number_of_nodes(self._map), "Marking a non existing node"
        if self._map.nodes[node].get("color") == START:
            return False
        elif self._map.nodes[node].get("color") == EXPLORATED:
            return False

        self._map.nodes[node]["color"] = EXPLORATED
        return True

    def explorated(self, node) -> bool:
        """ Check if a node is explorated """
        node = int(node)
        assert 0 <= node <= nx.number_of_nodes(self._map), "Marking a non existing node"
        return self._map.nodes[node].get("color") == START or self._map.nodes[node].get("color") == EXPLORATED

    def size(self) -> int:
        """ Get the size of the world """
        return nx.number_of_nodes(self._map)

    def cost(self, node_1, node_2) -> int:
        """ Get the cost between two nodes

        :node_1: Node id
        :node_2: NOde id
        :returns: The cost

        """
        return self._map[node_1][node_2]["weight"]

    def get_agents_numbers(self, node):
        """ Get the number of agents and a given node

        :node: The node id
        :returns: The number of agents

        """
        assert 0 <= node <= nx.number_of_nodes(self._map), "Get number of agents from a non existing node"
        ret = self._map.nodes[node].get("agents")
        if ret is None:
            return 0

        return ret

    def update_value(self, node: int, key: str, value):
        """ Update a value on a node

        :node: The node id
        :key: The key 
        :value: The value to assign

        """
        node = int(node)
        assert 0 <= node <= nx.number_of_nodes(self._map), "Updating value on a non existing node"
        self._map.nodes[node][key] = value

    def view(self, block=True, node_id=False, color_map=ClassicColor()):
        """ Show the world

        """
        color = self._map.nodes(data="color", default=UNEXPLORATED)
        color = [color_map(c) for _, c in color]

        if node_id:
            agents = self._map.nodes(data="agents", default=0)
            agents = {n: n for n, _ in agents}
        else:
            agents = self._map.nodes(data="agents", default=0)
            agents = {n: a for n, a in agents}

        pos = graphviz_layout(self._map, prog='neato')
        nx.draw_networkx(self._map, pos=pos, node_color=color, labels=agents)
        nx.draw_networkx_edge_labels(self._map, pos=pos,
                                     edge_labels=self._labels)
