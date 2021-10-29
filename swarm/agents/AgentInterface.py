""" The interface for a swarm agent """


class AgentInterface():
    """ Interface class for a swarm agent """

    def __init__(self, conf: dict, position: int):
        """ Create the agent

        :conf: The configuration of agent
        :position: The starting position of the agent

        """
        if conf is not None:
            assert type(conf) is dict, "The agent configuration must be of the type dict"

        if conf is None:
            conf = {'history': False,
                    'recrod': False,
                    'max_traveling_distance': -1}

        self._conf = conf
        self._position = position
        self._traveled_distance = 0

        if self._conf.get("history", False):
            self._history = []

        if self._conf.get("record", False):
            self._record = []

    def move(self, world, updated_pos) -> int:
        """ Move the agent

        :world: The world
        :updated_pos: The updated position of agents already moved
        :returns: The new node it would move to

        """
        return NotImplementedError("Swarm agents should contains this method")

    def record(self, information) -> None:
        """ Record the history of the agent

        :information: Information to record

        """
        if not self._conf.get("record", False):
            return

        self._record.append(information)

    @property
    def position(self) -> int:
        """ The position of the agent """
        return self._position

    @position.setter
    def position(self, new_position: int):
        """ Set the new position

        :new_position: The new node id

        """
        if self._conf.get("history", False):
            self._history.append(new_position)
        self._position = new_position

    @property
    def traveled_distance(self) -> int:
        """ Get the traveled distance of the agent """
        return self._traveled_distance

    @traveled_distance.setter
    def traveled_distance(self, value: int):
        """ Set the traveled distance """
        self._traveled_distance = value
