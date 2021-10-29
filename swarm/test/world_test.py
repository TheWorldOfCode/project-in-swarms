""" Testing the world class """
from swarm.world import WorldGenerator
import matplotlib.pyplot as plt


def main():
    """ Main test function """
    generator = WorldGenerator((10, 20), 1, (1, 11), seed=0)
    world = generator.generate()

    world.update_value(4, "agents", 4)
    
    # Checking if get the correct number of neighbors
    candidates = world.connected(4)
    assert len(candidates) == 3, "Error in the connected function, doesn't return the correct number of neighbors"

    # Testing if getting the correct number of agent in neight nodes
    for c in candidates:
        world.update_value(c, "agents", 1)

    total = 0
    for c in candidates:
        total += world.get_agents_numbers(c)
    
    assert total == 3, "Error in the get_agents_numbers function, doesn't return the correct number of agents"

    world.view()
    plt.show()


if __name__ == "__main__":
    main()
