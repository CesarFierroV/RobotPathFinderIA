
# API from RoboDK
from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

from robodk import *      # RoboDK API
from robolink import *    # Robot toolbox

# Import time to measure the time of the robot program
import time

#Import a library to sort lists
from operator import itemgetter

# Import the path_finder based on genetic algorithms
from pathFinder import path_finder, testBestPath

# Link to RoboDK
RDK = robolink.Robolink()


def main():
    # Define the origin and destination points
    HOME_POINT = RDK.Item('Home')
    ORIGIN_POINT =  RDK.Item('Origin')
    DESTINATION_POINT = RDK.Item('Destination')
    NPOP = 1200
    NUMBER_OF_POINTS = 5
    NGEN = 8

    # Generate an instance of the robot
    robot =RDK.Item('Fanuc M-900iB/700')

    # Cycle the training until find a decent fitness
    fitness = -80
    while fitness < -10:
        path = path_finder(robot,
                            ORIGIN_POINT, DESTINATION_POINT,
                            NPOP, NUMBER_OF_POINTS, NGEN)
        fitness = path[3]
        print('champ fitness', fitness)
     
    print(path[0])
    print(path[1])
    while(True):
        testBestPath(robot, path, ORIGIN_POINT, DESTINATION_POINT)


if __name__=="__main__": 
    main()