# Class that has all the information, funcions, modules to create a
# genetic algorithm for robot paths.

import random

#Import a library to sort lists
from operator import itemgetter

class GeneticAlgoritm:
    def __init__(self):
        #random.seed(1023)
        self.phenotypes = []

    def resetPopulation(self):
        self.phenotypes = []

    # Method to create the phenotypes
    # For this application the phenotypes will be the programs to test

    # The phenotypes will have in the genotype the number of points in them and the coordinates
    #    for every point
    #    index 0 = number of points
    #    index 1 = list containing coordinates of every point in index 0
    #    index 2 = stores if the points are Linear or Joint (not working for now)
    #    index 3 = will store the fitness of the individual
    #    index 4 = used to store the information of the path, used to get the fitness (collisions, not reachable points, axis and cartesian movment)

    def createEmptyPhenotypes(self, numberOfPhenotypes):

        phenotypeShape = [1, [2], 3, 4, [5]]
        
        for phenotype in range(0, numberOfPhenotypes):
            self.phenotypes.append([1, [2], 3, 4, [5]])


    # Create the genomas for the phenotype, returns a list with three elements, 
    def createGenes(self, maximumNumberOfPoints, bias_active):

        # We asign the genes (points and coordinates) to the phenotyes
        for phenotype in range(0, len(self.phenotypes)):

            pointsCoordinates = []

            # Define the number of points that the program will have
            numberOfPoints = int(random.uniform(1, maximumNumberOfPoints + 1))

            self.phenotypes[phenotype][0] = numberOfPoints

            # Define the coordinates of every point in XYZwpr format
            for point in range(1, numberOfPoints + 1):

                coordinatesXYZwpr = self.generateCoordinates(bias_active)
                pointsCoordinates.append(coordinatesXYZwpr)

            self.phenotypes[phenotype][1] = pointsCoordinates

            # We assign the last gen of the genoma to the phenotype (if the movment is Linear or Joint)
            isLinear = random.choice([True, False])
            if isLinear:
                self.phenotypes[phenotype][2] = 'L'
            else:
                self.phenotypes[phenotype][2] = 'J'
            

    def sortPhenotyopesByFitness(self):
        self.phenotypes = sorted(self.phenotypes, key=itemgetter(3), reverse=True)
        for i in self.phenotypes: print(i[3])

    def selectMostFitPhenotypes(self):
        self.mostFitPhenotypes = self.phenotypes[:int(len(self.phenotypes)/2)]

    # Note for the future add here a new method for tournament, instead of sorting and selecting phenotypes directly by score
    # There will be tournaments between 3 to 5 individuals and the best will pass to next generation
    # Then remaining individuals can or can not compete again
    def selectByTournament(self):

        # Elite individuals will pass automatically to next generation
        elitism = 6
        self.mostFitPhenotypes = self.phenotypes[0:elitism]

        numOfIndividualsPassingNextGen = int(len(self.phenotypes)/2) - elitism

        # Update the population without the elite
        self.phenotypes = self.phenotypes[elitism:]

        for i in range(0, numOfIndividualsPassingNextGen):
            tournamentCompetitors = random.choices(self.phenotypes, k=5)
            winner = (max(tournamentCompetitors, key=itemgetter(3)))
            self.mostFitPhenotypes.append(winner)

    def selectiveCrossover(self): # This selective crossover will give priority to the genes of the best parent
        random.shuffle(self.mostFitPhenotypes)

        # List to save next generation with the size of the most fit list
        self.nextPhenotypeGen = []
                                 
        for couple in range(0, len(self.mostFitPhenotypes), 2):

            # Define the next generation shape and resets the values
            nextGenPhenotypesChild1 = [1, [2], 3, 4, [5]]
            nextGenPhenotypesChild2 = [1, [2], 3, 4, [5]]

            parent1 = self.mostFitPhenotypes[couple]
            parent2 = self.mostFitPhenotypes[couple + 1]
            #print(parent1)
            #print("")
            #print(parent2)
            #print("**********************************")

            # Select best parent
            bestParent = max([parent1, parent2], key=itemgetter(3))
            worstParent = min([parent1, parent2], key=itemgetter(3))
            #print(bestParent)
            #print("")
            #print(worstParent)

            #print("**********************************")

            # First child will be identical to the best parent except for one random point
            #try:
                
            nextGenPhenotypesChild1[0], nextGenPhenotypesChild1[1] = bestParent[0], bestParent[1]
            nextGenPhenotypesChild1[1][int(random.uniform(0, len(bestParent[1])-1))] = random.choice(worstParent[1])
            #print(bestParent[1])
            #print(len(bestParent[1]))
            #print("**********************************")
                #if couple == 3 or couple ==5:
                    #print(bestParent[1], bestParent[2])
                    #print(len(bestParent[1]))
            #except:
                #if couple == 3 or couple ==5:

            # Second Child will be similar to worst parent but with the coordinates of first parent
            nextGenPhenotypesChild2[0], nextGenPhenotypesChild2[1] = worstParent[0], bestParent[1][0:worstParent[0]-1]
            
            nextGenPhenotypesChild1[2] = 'J'
            nextGenPhenotypesChild2[2] = 'L'

            self.nextPhenotypeGen.append(nextGenPhenotypesChild1)
            self.nextPhenotypeGen.append(nextGenPhenotypesChild2)

    def crossover(self):

        random.shuffle(self.mostFitPhenotypes)

        # List to save next generation with the size of the most fit list
        self.nextPhenotypeGen = []
                                 
        for couple in range(0, len(self.mostFitPhenotypes), 2):

            # Define the next generation shape and resets the values
            nextGenPhenotypesChild1 = [1, [2], 3, 4, [5]]
            nextGenPhenotypesChild2 = [1, [2], 3, 4, [5]]

            parent1 = self.mostFitPhenotypes[couple]
            parent2 = self.mostFitPhenotypes[couple + 1]

            # Select parent that will pass the number of points
            randomChoiceParentPointsToPass = random.choice([True, False])

            if randomChoiceParentPointsToPass:
                pointtsToBePassedByParent1 = parent1[0]
                pointtsToBePassedByParent2 = parent2[0]
                nextGenPhenotypesChild1[0] = parent1[0]
                nextGenPhenotypesChild2[0] = parent2[0]
            else:
                pointtsToBePassedByParent1 = parent2[0]
                pointtsToBePassedByParent2 = parent1[0]
                nextGenPhenotypesChild1[0] = parent2[0]
                nextGenPhenotypesChild2[0] = parent1[0]

            # Check for the parent to get who has less points and create the crossover point according to that
            minimalNumPoints = min(parent1[0], parent2[0])
            crossPoint = int(random.random()*minimalNumPoints)
            # If crosspoint is zero we make sure is at least one to ensure
            # One gen of every parent makes it to next gen
            if crossPoint == 0 : crossPoint = 1
            nextGenPhenotypesChild1[1] = parent1[1][:crossPoint] + parent2[1][crossPoint:pointtsToBePassedByParent1]
            nextGenPhenotypesChild2[1] = parent2[1][:crossPoint] + parent1[1][crossPoint:pointtsToBePassedByParent2]

            nextGenPhenotypesChild1[2] = 'J'
            nextGenPhenotypesChild2[2] = 'L'

            self.nextPhenotypeGen.append(nextGenPhenotypesChild1)
            self.nextPhenotypeGen.append(nextGenPhenotypesChild2)
    
    # Creates a method that can randolmy select a individual in the new generation
    # and mutates one or a few of its characteristics.
    def mutation(self, bias_active):
        for newPhenotype in self.nextPhenotypeGen:
            # Generate a random number between 1 and 10,
            # if the number is 7 a mutation will occur in the phenotype

            mutationRand = int((random.random()*10) + 1)

            mutationTrue = mutationRand == 7 or mutationRand == 5 or mutationRand == 3

            if mutationTrue:
                # Select what point in the program is going to change
                pointToMutate = int((random.random()*newPhenotype[0]-1))

                # Generate new coordinates for the mutated point
                coordinatesXYZwpr = self.generateCoordinates(bias_active)
                try:
                    newPhenotype[1][pointToMutate] = coordinatesXYZwpr
                except:
                    pass

    # Takes the mostfit phenotypes from the previous generation
    # And the new phenotypes and creates a new generation
    def createNewGeneration(self):
        self.phenotypes = self.mostFitPhenotypes + self.nextPhenotypeGen

    def shuffleGeneration(self):
        self.phenotype = random.shuffle(self.phenotypes)
    
    def generateCoordinates(self, bias_active):

        # Coordinates to define
        coordiantesToDefine = ['X', 'Y', 'Z', 'w', 'p', 'r']
        #Creates a list to store the coordinates of every point
        coordinatesXYZwpr = []
        for coordinate in coordiantesToDefine:

            # Get a random number and assigns it to a cartesian coordinate
            if coordinate in coordiantesToDefine[:3]:
                coordinateValue = random.random()*2000 #round(random.random()*2000, 3)
                # Defines if the value for the degree will be negative
                isNegative = random.choice([True, False])
                if isNegative:
                    coordinateValue = coordinateValue * (-1)

            # Get a random number and assigns it to a deegree
            if coordinate in coordiantesToDefine[3:]:
                coordinateValue = random.random()*180 #round(random.random()*180, 3)

                # Defines if the value for the degree will be negative
                isNegative = random.choice([True, False])
                if isNegative:
                    coordinateValue = coordinateValue * (-1)

            if bias_active:

                # Set a specific range for coordinates, bias the candidates towards the results we want
                X_range = (200, 1000) #
                Y_range = (-950, 1300) # Plane between Origin and Destination
                Z_range = (0, 1500) # Not used for now
                if coordinate == 'Y':
                    coordinateValue = random.uniform(Y_range[0], Y_range[1])
                if coordinate == 'X':
                    coordinateValue = random.uniform(X_range[0], X_range[1])
                if coordinate == 'Z':
                    coordinateValue = random.uniform(Z_range[0], Z_range[1])

            coordinatesXYZwpr.append(coordinateValue)
        return coordinatesXYZwpr
    

    def getCoordinatesOfThePhenotype():
        pass

    def calculateFitnessFunc(self):

        for phenotype in self.phenotypes:

            totalCollisions, totalNotReachPoints, totalAxisMovment, totalCartMovment, cycleTime = phenotype[4]

            collisionPunishment = 3
            notReachablePointPunishment = 5
            fitness = 0

            # Depending on the parameters we define the fitness
            fitness = fitness + (totalAxisMovment / (-10000))
            fitness = fitness + (totalCartMovment / (-5000))

            # Not reachable points punishment
            fitness = fitness - (totalNotReachPoints * notReachablePointPunishment)
        
            # Collision punisments
            fitness = fitness - (totalCollisions * collisionPunishment)
            if totalCollisions == 0:
                fitness = fitness + 1
            
            phenotype[3] = fitness
    
    def calculateFitnessFunc2(self, verbosity):

        for phenotype in self.phenotypes:

            fitness = 0 # initialize fitness

            totalCollisions, totalNotReachPoints, totalAxisMovment, totalCartMovment, cycleTime = phenotype[4]
            numberOfPoints = phenotype[0]
            numCollFreePoints = phenotype[0] + 1 - totalCollisions #phenotype[4] = number of points in program + 1 because of destination point

            #programCollFree = 0
            #if totalCollisions == 0: programCollFree = 1
            programCollFree = int(totalCollisions == 0)

            w1 = 0.3 # Weight for number of points free of collision
            w2 = 1 # Weight for program collision free
            w3 = 0.4 # weight for collisions found
            w4 = 0.8 # weight for not reachable points
            w5 = 1 # weight for total axis movment 
            w6 = 0.3 # weight for total number of points

            # TO ADD LATER
            # we can add a path tracker, the minor the distance to the destination
            # more fitness will get, points after that one will have to follow
            # if not fitness will decrease

            # Formula for normalized fitness
            fitness = w1*numCollFreePoints + w2*programCollFree - w3*totalCollisions - w4*totalNotReachPoints - w5*totalAxisMovment/-10000 - w6*numberOfPoints

            phenotype[3] = fitness
        
        if verbosity:
            averageFitnees = sum(itemgetter(3)(fitness) for fitness in self.phenotypes)/len(self.phenotypes)
            print('Average Fitness:', averageFitnees)
    
    def showfitnessDataChampion(self, champion):
        totalCollisions, totalNotReachPoints, totalAxisMovment, totalCartMovment, cycleTime = champion[4]
        print('Total colisiones: ', totalCollisions)
        print('Numero de puntos sin colision: ', champion[0] + 1 - totalCollisions)
        print('Puntos no alcanzables: ', totalNotReachPoints)


    def calculateFitness(self, verbosity=False):
        self.calculateFitnessFunc2(verbosity)

    def temporalSolutionUpdatePointsNumber(self):
        for phenotype in self.phenotypes:
            phenotype[0] = len(phenotype[1])
