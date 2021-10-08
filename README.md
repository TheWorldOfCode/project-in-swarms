# Project in Swarms
This code was developed doing a course. 

The project attempt to solve the traveling salesman problem, using a number of
"simple" agents. 

There exists many real problems which can be formulated as the traveling
salesman problem, such as exploration of an area, search and rescue and so on. 


The code contains a simple simulator, which is capable of  simulating the
swarm in discrete time steps.

## Running the simulation
There is two different ways to run the simulation. It is possible using
argument to generate the world and the swarm, run `python -m swarm run --help`
for help. 

A different method is using a script. It is possible to create a script file
which defines specific methods, which is then used to setup the simulation.

It is also possible to get a template by running `python -m swarm script
--get-example`

## Developing new agents
It is possible to easily developing new agents for the swarm. This is done by
getting a new class which is based on the `AgentInterface` class. It would be
possible to define new function. But don't override the `__init__` function,
furthermore should there exists a function called `move`

In the code below are there showed an example with a random agent.

``` python
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
```
