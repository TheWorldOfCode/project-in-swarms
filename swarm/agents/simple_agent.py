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

        \[\lambda_{ac} = \begin{cases}
                             \frac{1}{\eta}^{\alpha_c + 0.01} & \alpha_a \neq 0 \\
                             \frac{\sum_{\alpha_c \neq 0} \lambda}{\eta_{\alpha_c \neq 0}} & \alpha_c = 0
                        \end{cases}\]

    
        Where $\lambda_ac$ is the likelihood for candidate c based on agents.
        Where $\alpha_c$ is the number agents at the candidate.
        Where $\eta$ is the number of candidates.
        Where $\eta_{alpha_c \neq 0}$ is the number of candidates with agents.

        The likelihood for selecting note based on the if the node is explorated.

        \[\lambda_{ec} = \begin{cases}
                            \frac{1}{\Delta} & e_{c} = 0 \\
                            0 & e_{c} = 1
                        \end{cases}\]

        Where $\lambda_ec$ is the likelihood for candidate c based on if it is explorated.
        Where $\Delta$ is the number of explorated notes.
        Where $e_c$ is 1 if the candidate is explorated.

        The likelihood for not selecting node based on the cost of traveling to the node. 

        \[\lambda_{Cc} = \frac{\zeta_c}{\sum{\zeta_c}} \]

        Where $\lambda_{Cc} is the likelihood for candidate c based on the cost. 
        Where $\zeta_c$ is the travel cost for candidate c. 

        The complete likelihood for selecting the candidate is given as 

        \[ \lambda_c = \tau_1 \cdot \lambda_{ac} + \tau_2 \lambda{ec} - \tau_3 \cdot \lambda_{Cc} \]

        Where $\lambda_c$ is the likelihood for selecting candiate c
        Where $\tau_1$, $\tau_2$ amd $\tau_3$ is tuning paramenter and selecting the importants for each term. 

        This agent contains a single setting.
            - continously (boolean): Use the movement of alraady moved agents
                                     in the current turn
    """

    def __init__(self, conf, position):
        """ Create the agent

        :conf: The configuration of agent
        :position: The starting position of the agent

        """
        AgentInterface.__init__(self, conf, position)

        self._tau_1 = conf.get("tau_1", 1)
        self._tau_2 = conf.get("tau_2", 1)
        self._tau_3 = conf.get("tau_3", 0.5)

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
            if alpha != 0:
                likelihood[i] = (1/float(eta))**float(alpha + 0.01)
            else:
                likelihood[i] = 1

            if likelihood[i] != 1:
                sum_lamb += likelihood[i]
            else:
                lamb_2.append(i)

        if sum_lamb == 0:
            sum_lamb = 1

        for i in lamb_2:
            likelihood[i] = sum_lamb/len(lamb_2)

        logging.debug(f"Likelihood: {str(likelihood)}")

        if sum(likelihood) > 1:
            logging.warn(f"The sum is approve 1({sum(likelihood)}), likelihood {likelihood}, Alpha: {nr_agents}")

        return likelihood

    def exploration(self, nr_agents, explorated):
        """ Calculating the likelihood for selecting a node according if it is explored
            :nr_agents: Number of agents at each candidate
            :explorated: If a candidate is explorated
            :return: The likelihood
        """

        likelihood = [0] * len(nr_agents)

        for i, agent in enumerate(nr_agents):
            if not explorated[i] or agent > 0:
                likelihood[i] = 1

        s = sum(likelihood)
        if s != 0:
            for i in range(len(nr_agents)):
                likelihood[i] /= s

        logging.debug(f"Exploration likelihood: {likelihood}")

        return likelihood

    def cost(self, cost):
        """ The likelihood for not selecting a node according to the travel cost. 
        :cost: The travel cost
        :return: The likelihood
        """
        likelihood = [0] * len(cost)

        _max = max(cost)
        _min = min(cost)
        diff = _max - _min

        if diff != 0:
            for i, c in enumerate(cost):
                likelihood[i] = (c - _min)/(diff)

        return likelihood

    def move(self, world, updated_pos) -> int:
        """ Move the agent

        :world: The world
        :updated_pos: The updated position of agents already moved
        :returns: The new node it would move to

        """
        self.switch_state()
        canndidates = world.connected(self.position)
        cost = []
        explorated = []
        nr_agents = []
        for c in canndidates:
            explorated.append(world.explorated(c))
            cost.append(world.cost(self.position, c))
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
        a_likelihood = self.calculation(total, nr_agents)
        e_likelihood = self.exploration(nr_agents, explorated)
        c_likelihood = self.cost(cost)

        likelihood = [0] * len(nr_agents)
        i = 0
        for a, e, c in zip(a_likelihood, e_likelihood, c_likelihood):
            likelihood[i] = self._tau_1 * a + self._tau_2 * e - self._tau_3 * c
            i += 1

        _max = max(likelihood)
        _min = min(likelihood)
        if _max - _min != 0:
            for i, l in enumerate(likelihood):
                likelihood[i] = (l - _min)/(_max - _min)

        if self._conf.get('record', False):
            self.record({'alpha': nr_agents,
                         'explorated': explorated,
                         'cost': cost,
                         'likelihood': likelihood,
                         'agent_likelihood': a_likelihood,
                         'exploration_likelihood': e_likelihood,
                         'cost_likelihood': c_likelihood})

        new_position = rnd.choices(canndidates, weights=likelihood)[0]

        self.traveled_distance += world.cost(self.position, new_position)
        self.position = new_position

        self.switch_state()
        return self._position


def simple_agent_generator(conf=None) -> Callable:
    """ Create a simple agent generator

    :conf: The configuration
    :returns: A generator function

    """

    def generator():
        return SimpleAgent(conf, rnd.randint(0, 10))

    return generator
