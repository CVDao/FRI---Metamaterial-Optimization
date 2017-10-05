from deap import base, creator, tools, algorithms
import numpy
from pprint import pprint 

#200mm x 150mm
voxSize = 5  # in millimeters
length = 200/voxSize  #Calculates the size of the X Dimension of the array.
width = 150/voxSize   #Calculates the size of the Y dimension of the array.
#voxels assumed to be 5x5x5 mm
# a test comment
popSize = 20

		
def main():
	creator.create("FMax", base.Fitness, weights = (1.0,) )
	creator.create("Individual", list, fitness = creator.FMax)
	toolbox = base.Toolbox()
	toolbox.register("genIndividual", genInd, creator.Individual)
	pprint(genInd())

def genInd():
	fullHolder = []
	for i in range(len(length)):
		fullHolder.append([])
		for i in range(len(width)):
			fullHolder[i].append([1])
	return fullHolder
