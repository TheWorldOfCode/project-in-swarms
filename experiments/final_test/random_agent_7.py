from swarm.world import WorldGenerator
import swarm
import swarm.agents as agents
import argparse

global arguments


def args(unknown):
    global arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="results.yaml")

    arguments = parser.parse_args(unknown)


###############################
# THIS FUNCTION IS REQUIRED   #
# It is used to generate the  #
# the world.                  #
###############################
def world_generation():
    """ Create the world """
    world_generator = WorldGenerator((20, 50), 1, (1, 10), 10213)

    return world_generator.generate()


##################################
# THIS FUNCTION IS NOT REQUIRED  #
# It is used to generate the     #
# world.                         #
##################################

#def get_video_recorder():
#    """ Get the recorder of the simulations """
#    return swarm.VideoRecorder(1)

##################################
# THIS FUNCTION IS NOT REQUIRED  #
# It is used to save the result  #
##################################
def get_data_recorder():
    """ Save the data from the simuation to file """
    global arguments
    return swarm.AgentDataRecorder(arguments.out)


##################################
# THIS FUNCTION IS REQUIRED      #
# This is used to get the list   #
# of agents to spawn in swarm    #
##################################
def agent_generator_list():
    """ Get the list of agents to spawn """
    conf = {"history": True}
    gen = agents.random_agent_generator(conf)
    generators = [[20, gen]]

    return generators


##################################
# THIS FUNCTION IS REQUIRED      #
# This is used to get the list   #
# arguments to the simulation    #
##################################
def get_sim_args():
    """ Get the arguments to the simulation """
    return {
             'display': False,
             'speed': 1,
            }
