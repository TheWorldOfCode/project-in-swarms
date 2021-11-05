""" This module is used for debuggering the agents """
from .world import World, NoColor, ClassicColor
from cmd import Cmd

import matplotlib.pyplot as plt


class Debugger(Cmd):

    """ The debugger """

    prompt = ">> "
    intro = "Welcome! Type ? to list commands"

    def __init__(self, world: World, results):
        """ Create the debugger

            :world: The world used
            :results: The results from a data recorder
        """
        Cmd.__init__(self)
        self._world = world
        self._results = results

        self._get_discovered()

    def show_map(self, node_id, colormap):
        """ Show the map """
        self._world.view(False, node_id=node_id, color_map=colormap)
        plt.show(False)

    def _check_turn(self, turn: int) -> bool:
        """ Check if turn is available """
        if 0 <= turn <= int(self._results['turns']):
            return True

        print(f"There was no turn {turn}")

        return False

    def _check_node(self, node: int) -> bool:
        """ Check if turn is available """
        if 0 <= node <= int(self._results['nodes']):
            return True

        print(f"There was no node {node}")

        return False

    def _get_discovered(self):
        turns = int(self._results["turns"])
        agents = len(self._results['agents_history'])

        self._discovered = []
        
        #self._visists = [[False] * turns] * int(self._results['nodes'])

        self._visists = []
        for i in range(int(self._results['nodes'])):
            v = []
            for j in range(turns):
                v.append(False)
            self._visists.append(v)

        for i in range(turns):
            vis = []
            if len(self._discovered) != 0:
                dis = [s for s in self._discovered[-1]]
            else:
                dis = []

            for j in range(agents):
                dis.append(self._results['agents_history'][j][i])
                vis.append(self._results['agents_history'][j][i])

            for s in set(vis):
                self._visists[s][i] = True

            unique = [s for s in set(dis)]
            self._discovered.append(unique)

    def do_exit(self, inp):
        """ Exit prompt """
        return True

    def help_exit(self):
        print("Exit the debugger")

    def do_show(self, inp):
        """ Show the map """
        if len(inp) == 0:
            self.show_map(True, NoColor())
        else:
            args = inp.split(" ")
            if len(args) > 1:
                print("It takes only one argument")
            else:
                turn = int(args[0])
                if self._check_turn(turn):
                    self._world.reset()
                    for n in self._discovered[turn]:
                        self._world.explore(n)

                    self.show_map(True, ClassicColor())

    def help_show(self):
        print("Show the map\n\t usage: show [turn]\n\n If given a turn it would show the state of the turn")

    def do_node(self, inp):
        """ Show information about a node """
        args = inp.split(" ")

        for node in args:
            node = int(node)

            if self._check_node(node):
                print(f"Node {node}")
                for i, n in enumerate(self._discovered):
                    if node in n:
                        print(f"\tDiscovered in: {i}")
                        break
                s = ""
                for i, b in enumerate(self._visists[node]):
                    if b:
                        s += str(i)
                        s += " "

                print(f"\tVisists {s}")

    def help_node(self):
        print("Show basic information about nodes\n \tusage: info node ...")

    def do_turn(self, inp):
        """ Show information about a given turn """
        agents = len(self._results['agents_history'])
        args = inp.split(" ")

        for turn in args:
            turn = int(turn)

            if self._check_turn(turn):
                print(f"Turn {turn}")
                turns_agents = []
                for i in range(agents):
                    turns_agents.append(self._results['agents_history'][i][turn])

                for n in set(turns_agents):
                    print(f"\tNode {n} has {turns_agents.count(n)} agents")

    def help_turn(self):
        print("Show information about a turn\n\tusgae: turn turn_nr ...")

    def do_info(self, inp):
        """ Show information about a node at a given turn """

        args = inp.split(" ")

        if len(args) != 2:
            print("WRONG number of arguments")
            self.help_info()
        else:
            turn = int(args[0])
            node = int(args[1])

            print(f"Information about {node} at turn {turn}")

            if node in self._discovered[turn]:
                print("\t- Explorated")
            else:
                print("\t- Unexplorated")
            
            agents = []
            for i, agent in enumerate(self._results["agents_history"]):
                if int(agent[turn]) == node:
                    next = "Finished"
                    if turn < len(agent)-1:
                        next = f"Node {agent[turn + 1]}"
                    agents.append((i, next))

            if len(agents) == 0:
                print("\t- No agents at node")
            else:
                print("\t- Agents:")

                for agent, next in agents:
                    print(f"\t\t- Agent {agent} -> Move to {next}")
                    info = self._results["agents_record"][agent][turn]

                    for key in info:
                        value = info[key]
                        print(f"\t\t\t- {key}: {value}")


                

    def help_info(self):
        print("Show information about a node at a given turn\n\tusage: info turn node")
