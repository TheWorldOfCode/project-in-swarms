""" Main function """
import logging
import argparse
from random import seed

from .world import World, WorldGenerator
from .agent import random_agent_generator
from . import VideoRecorder, DummyRecorder
from . import Swarm
from . import Simulator


def args():
    parser = argparse.ArgumentParser(description="Solving the traveling Salesman problem using swarms.\n Autogenerate graph worlds with random weights and number of nodes")

    parser.add_argument("-n", "--nodes",
                        help="The minmum and maximum number of nodes in the world",
                        nargs=2, metavar=("min", "max"), type=int, required=True)

    parser.add_argument("-e", "--edge-multiplier",
                        help="The number of edges is determine by the number of edges times the multiplier",
                        nargs=1, metavar="multiplier", default=1, type=float)

    parser.add_argument("-c", "--edge-cost",
                        help="The range of cost between nodes",
                        nargs=2, metavar=("min", "max"), type=float,
                        default=(1, 10))
    parser.add_argument("--seed",
                        help="The seed for the autogeneration",
                        nargs=1, metavar="seed", type=int, default=seed())
    parser.add_argument("--delay",
                        help="The delay between each turn in the simulation (used together with display)",
                        nargs=1, metavar="delay", type=float, default=-1)
    parser.add_argument("-r", "--record",
                        help="Record a video of the simulation",
                        nargs=1, metavar="filename", type=str)

    parser.add_argument("-s", "--swarm",
                        help="The size of the swarm",
                        nargs=1, metavar="size", type=int, required=True)

    return parser.parse_args()


def main(args):
    """ Run the main loop """
    if type(args.swarm) == list:
        args.swarm = args.swarm[0]

    if type(args.delay) == list:
        args.delay = args.delay[0]

    logging.root.setLevel(logging.INFO)
    logging.info(f"Runtime arguments f{args}")

    #world_generator = WorldGenerator(10, 20, 1, (1, 10), 0)
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
    print(f"\tLowest traveling distance {results.highest}")

    if args.record is not None:
        recorder.save(args.record)


if __name__ == "__main__":
    main(args())
