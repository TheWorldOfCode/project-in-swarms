""" Main function """
import logging
import argparse
import os
import sys
import signal
import networkx as nx
from random import seed

from .world import World, WorldGenerator
from .agents import random_agent_generator
from . import VideoRecorder, DummyRecorder, DummyDataRecorder, BasicDataRecorder, DATA_RECORDER_LIST
from . import Swarm
from . import Simulator
from . import Debugger


def args():
    """ Handles the arguments """
    parser = argparse.ArgumentParser(description="Solving the traveling Salesman problem using swarms.\n Autogenerate graph worlds with random weights and number of nodes")

    subparsers = parser.add_subparsers(help="Commands")
    subparse_run = subparsers.add_parser("run", help="Run a experiment")

    subparse_run.add_argument("-n", "--nodes",
                              help="The minmum and maximum number of nodes in the world",
                              nargs=2, metavar=("min", "max"), type=int,
                              required=True)
    subparse_run.add_argument("-e", "--edge-multiplier",
                              help="The number of edges is determine by the number of edges times the multiplier",
                              nargs=1, metavar="multiplier", default=1,
                              type=float)
    subparse_run.add_argument("-c", "--edge-cost",
                              help="The range of cost between nodes",
                              nargs=2, metavar=("min", "max"), type=float,
                              default=(1, 10))
    subparse_run.add_argument("--seed",
                              help="The seed for the autogeneration",
                              nargs=1, metavar="seed", type=int,
                              default=seed())
    subparse_run.add_argument("--delay",
                              help="The delay between each turn in the simulation (used together with display)",
                              nargs=1, metavar="delay", type=float, default=-1)
    subparse_run.add_argument("-r", "--record",
                              help="Record a video of the simulation",
                              nargs=1, metavar="filename", type=str)
    subparse_run.add_argument("--data-recorder", help="Select data recoder for saving the result", 
                              choices=DATA_RECORDER_LIST)
    subparse_run.add_argument("-s", "--swarm",
                              help="The size of the swarm",
                              nargs=1, metavar="size", type=int, required=True)

    subparse_run.set_defaults(func=main)

    subparse_scripts = subparsers.add_parser("script", help="Load an experiment from script")
    group = subparse_scripts.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--load", nargs=1,
                       help="Script to load", metavar="filename",
                       type=str)
    group.add_argument("--get-example",
                       help="Get a example script", action="store_true")
    subparse_scripts.add_argument("--debug", help="Debug a result", nargs=1, type=str, default=None)

    subparse_scripts.set_defaults(func=scripts)

    subparse_tsp = subparsers.add_parser("tsp", help="Solve the traveling salesman problem")
    subparse_tsp.add_argument("-n", "--nodes",
                              help="The minmum and maximum number of nodes in the world",
                              nargs=2, metavar=("min", "max"), type=int,
                              required=True)
    subparse_tsp.add_argument("-e", "--edge-multiplier",
                              help="The number of edges is determine by the number of edges times the multiplier",
                              nargs=1, metavar="multiplier", default=1,
                              type=float)
    subparse_tsp.add_argument("-c", "--edge-cost",
                              help="The range of cost between nodes",
                              nargs=2, metavar=("min", "max"), type=float,
                              default=(1, 10))
    subparse_tsp.add_argument("--seed",
                              help="The seed for the autogeneration",
                              metavar="seed", type=int,
                              default=seed())
    group = subparse_tsp.add_mutually_exclusive_group(required=True)
    group.add_argument("--christofides", help="Solve TSP with chrisofides, approximation solution", action="store_true")
    group.add_argument("--traveling_salesman_problem", help="Find the shortest path", action="store_true")
    group.add_argument("--greedy_tsp", help="Finds low cost cycle", action="store_true")
    group.add_argument("--asadpour_tsp", action="store_true")
    
    group = subparse_tsp.add_mutually_exclusive_group(required=False)
    group.add_argument("--simulated-annealing-tsp", help="Optimize a solution", nargs=4, metavar=("temp", "max_itr", "N_inner", "alpha"))
    group.add_argument("--threshold-accepting-tsp", help="Optimize the solution", nargs=4, metavar=("thres", "max_itr", "N_inner", "alpha"))

    subparse_tsp.set_defaults(func=TSP)

    return parser.parse_known_args()


def interrupt_sim(signum, frame):
    """ Signal handler from CTRL+c for interrupting the simulation """
    global sim
    sim.interrupt()


def main(args, unknown):
    """ Run the main loop """
    global sim
    signal.signal(signal.SIGINT, interrupt_sim)
    if type(args.swarm) == list:
        args.swarm = args.swarm[0]

    if type(args.delay) == list:
        args.delay = args.delay[0]

    if type(args.seed) == list:
        args.seed = args.seed[0]

    if type(args.record) == list:
        args.record = args.record[0]

    logging.root.setLevel(logging.INFO)
    logging.info(f"Runtime arguments f{args}")

    world_generator = WorldGenerator(args.nodes, args.edge_multiplier,
                                     args.edge_cost, args.seed)

    world = world_generator.generate()

    gen = random_agent_generator()
    generators = [[args.swarm, gen]]
    swarm = Swarm(generators)
    swarm.set_positions(0)

    recorder = DummyRecorder()
    if args.record is not None:
        recorder = VideoRecorder(args.delay)

    data_recorder = DummyDataRecorder()

    if args.data_recorder is not None:
        data_recorder = getattr(sys.modules[__name__], args.data_recorder)()

    sim = Simulator(world,
                    display=args.delay != -1,
                    speed=args.delay, recording=recorder)
    sim.start(swarm)

    summary(sim, swarm, data_recorder)

    if args.record is not None:
        recorder.save(args.record)

    return 0


def summary(simulation: Simulator, swarm: Swarm, save_data):
    """ The summery after the simulation

    :simulation: The simulation
    :swarm: The swarm
    :save_data: The data recorder

    """
    sim_result = simulation.get_results()
    swarm_result = swarm.summary()
    print()
    print()
    print(sim_result)
    print()
    print(swarm_result)

    save_data.save(simulation, swarm)


def scripts(args, unknown):
    """ The main function when using scripts """

    if args.debug is not None:
        import importlib.machinery as imp
        import yaml
        script = args.load[0]
        script_module_loader = imp.SourceFileLoader("script", script)
        script_module = script_module_loader.load_module()

        if not hasattr(script_module, "world_generation"):
            logging.fatal("The script is missing the function world_generation, to generate the world")
            return 1

        world = script_module.world_generation()

        with open(args.debug[0], "r") as f:
            info = yaml.load(f)

        debugger = Debugger(world, info)
        debugger.cmdloop()
    elif args.load is not None:
        global sim
        signal.signal(signal.SIGINT, interrupt_sim)
        import importlib.machinery as imp

        logging.root.setLevel(logging.INFO)
        logging.info(f"Runtime arguments f{args}")
        script = args.load[0]
        if os.path.exists(script):
            logging.info(f"Loading {script}")
            script_module_loader = imp.SourceFileLoader("script", script)
            script_module = script_module_loader.load_module()

            if hasattr(script_module, "args"):
                script_module.args(unknown)
            else:
                if len(unknown) != 0:
                    logging.fatal(f"Unknown args {unknown}")
                    return 1

            if not hasattr(script_module, "world_generation"):
                logging.fatal("The script is missing the function world_generation, to generate the world")
                return 1
            elif not hasattr(script_module, "agent_generator_list"):
                logging.fatal("The script is missing the function agent_generator_list, to generate list of geneators for the swarm")
                return 1
            elif not hasattr(script_module, "get_sim_args"):
                logging.fatal("The script is missing the function get_sim_args, to get the arguments to the simulation")
                return 1

            world = script_module.world_generation()
            gen_list = script_module.agent_generator_list()
            sim_args = script_module.get_sim_args()
            recorder = DummyRecorder()
            recorder_filename = None
            save_data = DummyDataRecorder()
            if hasattr(script_module, "get_video_recorder"):
                recorder, recorder_filename = script_module.get_video_recorder()
            if hasattr(script_module, "get_data_recorder"):
                save_data = script_module.get_data_recorder()

            swarm = Swarm(gen_list)
            swarm.set_positions(0)

            sim = Simulator(world, recording=recorder, **sim_args)
            sim.start(swarm)

            summary(sim, swarm, save_data)

            if recorder_filename is not None:
                recorder.save(recorder_filename)

        else:
            logging.fatal(f"Could not find {script}")
            return 1
    elif args.get_example:

        from .example import get_example

        sys.stdout.write(get_example())


def TSP(args, unknown):
    """ Solve the travel salesman problem """
    logging.root.setLevel(logging.INFO)
    logging.info(f"Runtime arguments f{args}")

    world_generator = WorldGenerator(args.nodes, args.edge_multiplier,
                                     args.edge_cost, args.seed)

    world = world_generator.generate()
    world.full_connected()
    world.switch()

    if args.christofides:
        path = nx.approximation.traveling_salesman_problem(world._map)
    elif args.traveling_salesman_problem:
        path = nx.approximation.traveling_salesman_problem(world._map)
        pass
    elif args.greedy_tsp:
        path = nx.approximation.greedy_tsp(world._map)
    elif args.asadpour_tsp:
        path = nx.approximation.all_pairs_node_connectivity(world._map)
    
    op_path = None
    if len(args.simulated_annealing_tsp) != 0:
        temp, max_itr, N_inner, alpha = args.simulated_annealing_tsp
        op_path = nx.approximation.simulated_annealing_tsp(world._map, path,
                                                           temp=int(temp),
                                                           max_iterations=int(max_itr),
                                                           N_inner=int(N_inner),
                                                           alpha=float(alpha))
    elif len(args.threshold_accepting_tsp) != 0:
        thres, max_itr, N_inner, alpha = args.simulated_annealing_tsp
        op_path = nx.approximation.threshold_accepting_tsp(world._map, path,
                                                           thres=int(thres),
                                                           max_iterations=int(max_itr),
                                                           N_inner=int(N_inner),
                                                           alpha=float(alpha))

    print("Solution:", path)
    print("Cost: ", world.calc_cost_path(path))

    if op_path is not None:
        print("Optimized solution:", op_path)
        print("Cost:", world.calc_cost_path(op_path))


if __name__ == "__main__":
    arg, unknown = args()
    arg.func(arg, unknown)
