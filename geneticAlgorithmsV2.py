# Class that has all the information, funcions, modules to create a
# genetic algorithm for robot paths.

import random

#Import a library to sort lists
from operator import itemgetter

class GeneticAlgoritm:
    def __init__(self):
        self.phenotypes = []

    # Method to create the phenotypes
    # For this application the phenotypes will be the programs to test

    # The phenotypes will have in the genotype the number of points in them and the coordinates
    #    for every point
    def createEmptyPhenotypes(self, numberOfPhenotypes):

        phenotypeShape = [1, [2], 3]
        
        for phenotype in range(0, numberOfPhenotypes):
            self.phenotypes.append([1, [2], 3, 4, 5])


    # Create the genomas for the phenotype, returns a list with three elements, 
    def createGenes(self, maximumNumberOfPoints):

        # We asign the genes (points and coordinates) to the phenotyes
        for phenotype in range(0, len(self.phenotypes)):

            pointsCoordinates = []

            # Define the number of points that the program will have
            numberOfPoints = int(random.random()*(maximumNumberOfPoints - 1)) + 1

            self.phenotypes[phenotype][0] = numberOfPoints

            # Define the coordinates of every point in XYZwpr format
            for point in range(1, numberOfPoints + 1):

                coordinatesXYZwpr = self.generateCoordinates()
                pointsCoordinates.append(coordinatesXYZwpr)

            self.phenotypes[phenotype][1] = pointsCoordinates

            # We assign the last gen of the genoma to the phenotype (if the movment is Linear or Joint)
            isLinear = random.choice([True, False])
            if isLinear:
                self.phenotypes[phenotype][2] = 'L'
            else:
                self.phenotypes[phenotype][2] = 'J'
            

    def sortPhenotyopesByFitness(self):
        self.phenotypes = sorted(self.phenotypes, key=itemgetter(3))

    def selectMostFitPhenotypes(self):
        self.mostFitPhenotypes = self.phenotypes[int(len(self.phenotypes)/2):]

    def crossover(self):

        nextGenShape = [1, [2], 3, 4]

        # List to save next generation with the size of the most fit list
        self.nextPhenotypeGen = []
                                 
        for couple in range(0, len(self.mostFitPhenotypes), 2):

            # Define the next generation shape and resets the values
            nextGenPhenotypesChild1 = [1, [2], 3, 4]
            nextGenPhenotypesChild2 = [1, [2], 3, 4]

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
    def mutation(self):
        for newPhenotype in self.nextPhenotypeGen:
            # Generate a random number between 1 and 10,
            # if the number is 7 a mutation will occur in the phenotype

            mutationRand = int((random.random()*10) + 1)

            mutationTrue = mutationRand == 7 or mutationRand == 5 or mutationRand == 3

            if mutationTrue:
                # Select what point in the program is going to change
                pointToMutate = int((random.random()*newPhenotype[0]-1))

                # Generate new coordinates for the mutated point
                coordinatesXYZwpr = self.generateCoordinates()
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
    
    def generateCoordinates(self):

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

            coordinatesXYZwpr.append(coordinateValue)
        return coordinatesXYZwpr
    

    def getCoordinatesOfThePhenotype():
        pass
