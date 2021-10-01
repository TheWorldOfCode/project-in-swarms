""" The interface for a swarm agent """


class AgentInterface():
    """ Interface class for a swarm agent """

    def __init__(self, conf, position: int):
        """ Create the agent

        :conf: The configuration of agent
        :position: The starting position of the agent

        """
        self._conf = conf
        self._position = position
        self._traveled_distance = 0

    def move(self, world) -> int:
        """ Move the agent

        :world: The world
        :returns: The new node it would move to

        """
        return NotImplementedError("Swarm agents should contains this method")

    @property
    def position(self) -> int:
        """ The position of the agent """
        return self._position

    @position.setter
    def position(self, new_position: int):
        """ Set the new position

        :new_position: The new node id

        """
        self._position = new_position

    @property
    def traveled_distance(self) -> int:
        """ Get the traveled distance of the agent """
        return self._traveled_distance

    @traveled_distance.setter
    def traveled_distance(self, value: int):
        """ Set the traveled distance """
        self._traveled_distance = value
