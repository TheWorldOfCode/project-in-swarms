""" Main function """
import logging
import argparse
import os
import sys
from random import seed

from .world import World, WorldGenerator
from .agents import random_agent_generator
from . import VideoRecorder, DummyRecorder
from . import Swarm
from . import Simulator


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

    subparse_scripts.set_defaults(func=scripts)

    return parser.parse_args()


def main(args):
    """ Run the main loop """
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

    sim = Simulator(world,
                    display=args.delay != -1,
                    speed=args.delay, recording=recorder)
    results = sim.start(swarm)

    half = 0
    turn = 0
    for i, t in enumerate(results.discovered):
        half += t
        if half >= results.nodes/2:
            turn = i
            break

    print()
    print()
    print("Simulations result")
    print(f"\tNumber of turns: {results.turns}")
    print(f"\tNumber of nodes: {results.nodes}")
    print(f"\tAbove 50% at turn: {turn}")
    print()
    results = swarm.summary()
    print("Swarm summary")
    print(f"\tLowest traveling distance {results.lowest}")
    print(f"\tMean traveling distance {results.mean} (±{results.std})")
    print(f"\tHighest traveling distance {results.highest}")

    if args.record is not None:
        recorder.save(args.record)

    return 0


def scripts(args):
    """ The main function when using scripts """

    if args.load is not None:
        import importlib.machinery as imp

        logging.root.setLevel(logging.INFO)
        logging.info(f"Runtime arguments f{args}")
        script = args.load[0]
        if os.path.exists(script):
            logging.info(f"Loading {script}")
            script_module_loader = imp.SourceFileLoader("script", script)
            script_module = script_module_loader.load_module()

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

            print(sim_args)
            if hasattr(script_module, "get_video_recorder"):
                recorder = script_module.get_video_recorder()

            swarm = Swarm(gen_list)
            swarm.set_positions(0)

            sim = Simulator(world, recording=recorder, **sim_args)
            results = sim.start(swarm)

            half = 0
            turn = 0
            for i, t in enumerate(results.discovered):
                half += t
                if half >= results.nodes/2:
                    turn = i
                    break

            print()
            print()
            print("Simulations result")
            print(f"\tNumber of turns: {results.turns}")
            print(f"\tNumber of nodes: {results.nodes}")
            print(f"\tAbove 50% at turn: {turn}")
            print()
            results = swarm.summary()
            print("Swarm summary")
            print(f"\tLowest traveling distance {results.lowest}")
            print(f"\tMean traveling distance {results.mean} (±{results.std})")
            print(f"\tLowest traveling distance {results.highest}")

        else:
            logging.fatal(f"Could not find {script}")
            return 1
    elif args.get_example:

        from .example import get_example

        sys.stdout.write(get_example())




if __name__ == "__main__":
    arg = args()
    arg.func(arg)
