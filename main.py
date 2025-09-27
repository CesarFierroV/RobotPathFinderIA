
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
    NPOP = 60
    NUMBER_OF_POINTS = 2
    NGEN = 5

    # Generate an instance of the robot
    robot =RDK.Item('Fanuc ARC Mate 120iC')

    # Cycle the training until find a decent fitness
    fitness = -10
    while fitness < -3:
        path = path_finder(robot,
                            ORIGIN_POINT, DESTINATION_POINT,
                            NPOP, NUMBER_OF_POINTS, NGEN)
        fitness = path[3]
    
    # Crear un nuevo algoritmo que genere los fenotipos en base al punto actual del robot
    # Empezando desde el origen crea un nuevo punto y se dirige a el, de este nuevo punto crea un nuevo punto
    # y se dirige a el, asi el n numero de puntos que contenga el fenotipo
    # Asi se pueden generar puntos mas cercanos, con menos distancia cartesiana y menos movimiento de los ejes
    # que generando los puntos random
    # se pueden definir un rango de solo +- 10 grados para generar el siguiente punto
    
    print(path[1])
    while(True):
        testBestPath(robot, path, ORIGIN_POINT, DESTINATION_POINT)


if __name__=="__main__": 
    main()