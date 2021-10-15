""" Get a script example """


def get_example():
    """ Get the example """
    return """ 
from swarm.world import WorldGenerator
import swarm
import swarm.agents as agents


###############################
# THIS FUNCTION IS REQUIRED   #
# It is used to generate the  #
# the world.                  #
###############################
def world_generation():
    \"\"\" Create the world \"\"\"
    world_generator = WorldGenerator((10, 20), 1, (1, 10), 0)

    return world_generator.generate()


##################################
# THIS FUNCTION IS NOT REQUIRED  #
# It is used to set the recorder #
# and the filename to save to    #
##################################

#def get_video_recorder():
#    \"\"\" Get the recorder of the simulations \"\"\"
#    return swarm.VideoRecorder(1), "filename.mp4"

##################################
# THIS FUNCTION IS NOT REQUIRED  #
# It is used to save the result  #
##################################
#def get_data_recorder():
#    \"\"\" Save the data from the simuation to file \"\"\"
#    return swarm.BasicDataRecorder(\"results.yaml\")


##################################
# THIS FUNCTION IS REQUIRED      #
# This is used to get the list   #
# of agents to spawn in swarm    #
##################################
def agent_generator_list():
    \"\"\" Get the list of agents to spawn \"\"\"
    gen = agents.random_agent_generator()
    generators = [[10, gen]]

    return generators


##################################
# THIS FUNCTION IS REQUIRED      #
# This is used to get the list   #
# arguments to the simulation    #
##################################
def get_sim_args():
    \"\"\" Get the arguments to the simulation \"\"\"
    return {
             'display': True,
             'speed': 1,
            }
"""
