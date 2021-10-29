""" A simple agent only according number of other agents """
from . AgentInterface import AgentInterface

import random as rnd
from typing import Callable

import logging


class SimpleAgent(AgentInterface):

    """ A simple walk agent

        It accordings for the agents at each possible candidate,
        by calculating the likelihood for each candidate.


        The likelihood is divided into two parts, depending on
        if there is already agents at a candidate.

        \[\lambda_{c} = \begin{case}
                             \frac{1}{\eta}^{\alpha_c} & \alpha_c \neq 0 \\
                             \frac{\sum_{\alpha_c \neq 0} \lambda}{\eta_{\alpha_c \neq 0} & \alpha_c = 0
                        \end{case}\]

        Where $\lambda_c$ is the likelihood for candidate c.
        Where $\alpha_c$ is the number agents at the candidate.
        Where $\eta$ is the number of candidates.
        Where $\eta_{alpha_c \neq 0}$ is the number of candidates with agents.


        This agent contains a single setting.
            - continously (boolean): Use the movement of alraady moved agents
                                     in the current turn
    """

    def calculation(self, total, nr_agents):
        """ Calculating the likelihood of selecting a candidate.

        :total: The total number of agents
        :nr_agents: Number of agents at each candidate
        :returns: A list of likelihood for selecting a candidate

        """
        eta = len(nr_agents)
        likelihood = [0] * eta

        sum_lamb = 0
        lamb_2 = []
        for i, alpha in enumerate(nr_agents):
            likelihood[i] = (1/float(eta))**float(alpha)
            if likelihood[i] != 1:
                sum_lamb += likelihood[i]
            else:
                lamb_2.append(i)
            
        if sum_lamb == 0:
            sum_lamb = 1

        for i in lamb_2:
            likelihood[i] = sum_lamb/len(lamb_2)

        logging.debug(f"Likelihood: {str(likelihood)}")

        if self._conf.get('record', False):
            self.record(likelihood)
        
        if sum(likelihood) > 1:
            logging.warn(f"The sum is approve 1, likelihood {likelihood}, Alpha: {nr_agents}")

        return likelihood

    def move(self, world, updated_pos) -> int:
        """ Move the agent

        :world: The world
        :updated_pos: The updated position of agents already moved
        :returns: The new node it would move to

        """
        canndidates = world.connected(self.position)

        nr_agents = []
        for c in canndidates:
            agents = world.get_agents_numbers(c)
            if self._conf.get('continously', True):
                for old, new in updated_pos:
                    if c == old:
                        agents -= 1
                    elif c == new:
                        agents += 1

            if agents < 0:
                agents = 0
            nr_agents.append(agents)

        total = sum(nr_agents)
        likelihood = self.calculation(total, nr_agents)
        new_position = rnd.choices(canndidates, weights=likelihood)[0]

        self.traveled_distance += world.cost(self.position, new_position)
        self.position = new_position

        return self._position


def simple_agent_generator(conf=None) -> Callable:
    """ Create a simple agent generator

    :conf: The configuration
    :returns: A generator function

    """

    def generator():
        return SimpleAgent(conf, rnd.randint(0, 10))

    return generator
