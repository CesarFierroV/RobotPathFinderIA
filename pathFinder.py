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

# Import the class to create the genetic algorithm
from geneticAlgorithms import GeneticAlgoritm

# Create an instance of the GeneticAlgorithms class
geneticAlgorithm = GeneticAlgoritm()

# Define the test and fitnness funtion
def getFitness(robot, ORIGIN_POINT, DESTINATION_POINT):
    fitness = 0
    # Define punishments
    collisionPunishment = 3
    notReachablePointPunishment = 5

    # Test all the phenotypes in the current generation
    for phenotypeProgram in geneticAlgorithm.phenotypes:

        # Initializate variables/parameters for fitness for every phenotype
        TotalAxisMovment = 0
        totalCartMovment = 0
        collisionCounter = 0
        fitness = 0

        CycleTimeInit = time.perf_counter()

        # Move robot to Origin position to start path testing
        robot.MoveJ(ORIGIN_POINT)
        
        for pointCoordinates in phenotypeProgram[1]:#phenotypeProgram[1]:

            # Initializate local variables/parameters for fitness for very point
            AxMovPointToPoint = 0
            CartdMovPointToPoint = 0

            # Stores actual robot position in a 6 list representing the axes
            oldPointJoint = robot.Joints().list()

            # Store actual robot pos in XYZwpr Format
            oldCartesianValue = Pose_2_Fanuc(robot.Pose())

            # Convert new point coordinates XYZwpr to robot Pose Mat
            viaPoint = Fanuc_2_Pose(pointCoordinates)

            # Move Robot
            try:
                # Move robot to next point
                robot.MoveJ(viaPoint)

                # Test robots for collisions
                if robot.MoveJ_Test(oldPointJoint, robot.Joints().list()) == 0:
                    pass
                    #fitness = fitness + 1
                else:
                    collisionCounter = collisionCounter + collisionPunishment
                
                robot.MoveJ(viaPoint)
            except:
                fitness = fitness - notReachablePointPunishment

            # Get the difference in the axis movments
            AxMovPointToPoint = getAxisDifference(oldPointJoint, robot.Joints().list())
            TotalAxisMovment = TotalAxisMovment + AxMovPointToPoint

            # Get the difference in the cartesian plane
            CartdMovPointToPoint = getCartesianDifference(oldCartesianValue, Pose_2_Fanuc(robot.Pose()))
            totalCartMovment = totalCartMovment + CartdMovPointToPoint
        

        # Destination position
        try:
            oldPointJoint = robot.Joints().list()
            robot.MoveJ(DESTINATION_POINT)
            if robot.MoveJ_Test(oldPointJoint, robot.Joints().list()) == 0:
                pass
                #fitness = fitness + 1
            else:
                collisionCounter = collisionCounter + collisionPunishment
                
            
            robot.MoveJ(DESTINATION_POINT)

            # Get the difference in the axis movments
            AxMovPointToPoint = getAxisDifference(oldPointJoint, robot.Joints().list())
            TotalAxisMovment = TotalAxisMovment + AxMovPointToPoint

            # Get the difference in the cartesian plane
            CartdMovPointToPoint = getCartesianDifference(oldCartesianValue, Pose_2_Fanuc(robot.Pose()))
            totalCartMovment = totalCartMovment + CartdMovPointToPoint
        # If the program has a no reachable
        except:
            fitness = fitness - notReachablePointPunishment
        
        # Time in seconds
        CycleTimeFinish = time.perf_counter()
        CycleTime  = CycleTimeFinish - CycleTimeInit

        # Counter punishments
        fitness = fitness - collisionCounter
        if collisionCounter == 0:
            fitness = fitness + 1
        
        # Depending on the parameters we define the fitness
        fitness = fitness + (TotalAxisMovment / (-10000))
        fitness = fitness + (totalCartMovment / (-5000))

        # Save the fitness
        phenotypeProgram[3] = fitness
        averageFitnees = 0
        for phen in geneticAlgorithm.phenotypes:
            averageFitnees = averageFitnees + phen[3]
    print('average fitness: '  + str(averageFitnees / len(geneticAlgorithm.phenotypes)))
    

def sortByAxisMovments(phenothypesList):
    phenothypesList = sorted(phenothypesList, key=itemgetter(5))


def getCartesianDifference(coord1, coord2):
    cartesianMovList = []
    for i in range(0, 3):
        cartesianMovList.append(abs(coord1[i] - coord2[i]))
    cartesianMov = sum(cartesianMovList)
    #print('cartMov: ' + str(cartesianMov))
    return cartesianMov

def getAxisDifference(pos1, pos2):
    AxMovPointToPointList = []
    for i in range(0, 6):
        AxMovPointToPointList.append(abs(pos1[i] - pos2[i]))
    AxMovPointToPoint = sum(AxMovPointToPointList)
    #print('AxMov: ' + str(AxMovPointToPoint))
    return AxMovPointToPoint


# Defining path_finder function 
def path_finder(robot, originPoint, destinationPoint, NPOP=200, NUMBER_OF_POINTS=5, NGEN=10):

    # Create the Phenotypes and their genomas
    geneticAlgorithm.createEmptyPhenotypes(NPOP)
    geneticAlgorithm.createGenes(NUMBER_OF_POINTS)

    highestFitness = -1000

    for i in range(0, NGEN):
        print('Generation: ' + str(i + 1))
        getFitness(robot, originPoint, destinationPoint)

        # Sort the phenotypes by fitness
        geneticAlgorithm.sortPhenotyopesByFitness()

        # Obtain the most fit phenotypes
        #geneticAlgorithm.selectMostFitPhenotypes()

        # obtain parents by selecting them by tournament
        geneticAlgorithm.selectByTournament()

        geneticAlgorithm.crossover()

        # Mutation has a 3 out 10 chances to be true, need to increase that? Start doinig it in last generations if fitness is too low
        geneticAlgorithm.mutation()
        geneticAlgorithm.createNewGeneration()
        #geneticAlgorithm.shuffleGeneration()
    getFitness(robot, originPoint, destinationPoint)

    
    for individual in geneticAlgorithm.phenotypes:
        if individual[3] > highestFitness:
            mostFitIndividual = individual
            highestFitness = individual[3]
  
    print(mostFitIndividual[3])
    return  mostFitIndividual

def testBestPath(robot, mostFitPhenotype, originPoint, destinationPoint):
    robot.MoveJ(originPoint)
    for pointCoordinates in mostFitPhenotype[1]:
        viaPoint = Fanuc_2_Pose(pointCoordinates)
        robot.MoveJ(viaPoint)

    robot.MoveJ(destinationPoint)