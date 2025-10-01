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



# Defining path_finder function 
def path_finder(robot, originPoint, destinationPoint, NPOP=200, NUMBER_OF_POINTS=5, NGEN=10):

    activate_bias = False

    # Create the Phenotypes and their genomas
    geneticAlgorithm.createEmptyPhenotypes(NPOP)
    geneticAlgorithm.createGenes(NUMBER_OF_POINTS, bias_active=activate_bias)

    highestFitness = -1000

    for i in range(0, NGEN):
        print('Generation: ' + str(i + 1))
        testPaths(robot, originPoint, destinationPoint) # test all the individuals and stores the fitness for everyone

        # gets and stores the fitness of every individual and saves it in index [3]
        geneticAlgorithm.calculateFitness()

        #geneticAlgorithm
        #sum_of_second_elements = sum(itemgetter(3)(fitness) for fitness in geneticAlgorithm.phenotypes)
        averageFitnees = sum(itemgetter(3)(fitness) for fitness in geneticAlgorithm.phenotypes)/len(geneticAlgorithm.phenotypes)
        print('Average Fitness:', averageFitnees)

        mostFitIndividual = max(geneticAlgorithm.phenotypes, key=itemgetter(3))
        print("Champ gen fitnesss: ", mostFitIndividual[3])
        if mostFitIndividual[3] > 1:
            break

        # Sort the phenotypes by fitness
        geneticAlgorithm.sortPhenotyopesByFitness()

        # obtain parents by selecting them by tournament
        geneticAlgorithm.selectByTournament()
        geneticAlgorithm.selectiveCrossover()
        geneticAlgorithm.mutation(bias_active=activate_bias)

        geneticAlgorithm.createNewGeneration()
        geneticAlgorithm.temporalSolutionUpdatePointsNumber()

    #print('Generation: ' + str(NGEN)
    testPaths(robot, originPoint, destinationPoint)
    # gets and stores the fitness of every individual and saves it in index [3]
    geneticAlgorithm.calculateFitness()
    mostFitIndividual = max(geneticAlgorithm.phenotypes, key=itemgetter(3))
    print("Champ gen fitnesss: ", mostFitIndividual[3])

    return  mostFitIndividual


# Define the test and fitnness funtion
def testPaths(robot, ORIGIN_POINT, DESTINATION_POINT):

    # Test all the phenotypes in the current generation
    for phenotypeProgram in geneticAlgorithm.phenotypes:

        # Initializate variables/parameters for fitness for every phenotype
        totalAxisMovment = 0
        totalCartMovment = 0
        collisionCounter = 0
        notReachablepoints = 0

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
                else:
                    collisionCounter = collisionCounter + 1
                
                robot.MoveJ(viaPoint)
            except:
                notReachablepoints = notReachablepoints + 1

            # Get the difference in the axis movments
            AxMovPointToPoint = getAxisDifference(oldPointJoint, robot.Joints().list())
            totalAxisMovment = totalAxisMovment + AxMovPointToPoint

            # Get the difference in the cartesian plane
            CartdMovPointToPoint = getCartesianDifference(oldCartesianValue, Pose_2_Fanuc(robot.Pose()))
            totalCartMovment = totalCartMovment + CartdMovPointToPoint
        
        # Destination position
        try:
            oldPointJoint = robot.Joints().list()
            robot.MoveJ(DESTINATION_POINT)
            if robot.MoveJ_Test(oldPointJoint, robot.Joints().list()) == 0:
                pass
            else:
                collisionCounter = collisionCounter + 1
                
            
            robot.MoveJ(DESTINATION_POINT)

            # Get the difference in the axis movments
            AxMovPointToPoint = getAxisDifference(oldPointJoint, robot.Joints().list())
            totalAxisMovment = totalAxisMovment + AxMovPointToPoint

            # Get the difference in the cartesian plane
            CartdMovPointToPoint = getCartesianDifference(oldCartesianValue, Pose_2_Fanuc(robot.Pose()))
            totalCartMovment = totalCartMovment + CartdMovPointToPoint
        # If the program has a no reachable
        except:
            notReachablepoints = notReachablepoints + 1
        
        # Time in seconds
        CycleTimeFinish = time.perf_counter()
        CycleTime  = CycleTimeFinish - CycleTimeInit

        # Store individual movments features 
        phenotypeProgram[4] = [collisionCounter, notReachablepoints, totalAxisMovment, totalCartMovment, CycleTime]
        #phenotypeProgram[3] = geneticAlgorithm.getFitnessFunc(collisionCounter, notReachablepoints, totalAxisMovment, totalCartMovment, CycleTime)

    

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


def testBestPath(robot, mostFitPhenotype, originPoint, destinationPoint):
    robot.MoveJ(originPoint)
    for pointCoordinates in mostFitPhenotype[1]:
        viaPoint = Fanuc_2_Pose(pointCoordinates)
        robot.MoveJ(viaPoint)

    robot.MoveJ(destinationPoint)
    #mostFitPhenotype[1].reverse()

    # reverse path
    #for pointCoordinates in mostFitPhenotype[1]:
    #    viaPoint = Fanuc_2_Pose(pointCoordinates)
    #    robot.MoveJ(viaPoint)
    
    #robot.MoveJ(originPoint)

def showMostFitIndividualInfo(champion):
    geneticAlgorithm.showfitnessDataChampion(champion)
    