from deap import base, creator, tools, algorithms
import numpy as np
from pprint import pprint 

#200mm x 150mm
voxSize = 5  # in millimeters
length = 200/voxSize  #Calculates the size of the X Dimension of the array.
width = 150/voxSize   #Calculates the size of the Y dimension of the array.
#voxels assumed to be 5x5x5 mm
# a test comment
popSize = 20

def genInd():
	fullHolder = []
	for i in range(0, width): #for ever row
		fullHolder.append(0) #add 2 0's at the start of the col
		fullHolder.append(0)
		for j in range(0, length): # add actual randomized bits
			fullHolder.append(np.random.randint(0,2))
		fullHolder.append(0) #add 2 0's at the end 
		fullHolder.append(0)
	teethY = width/2
	fullHolder[(teethY+1)*length] = 1
	fullHolder[(teethY-1)*length] = 1
	return fullHolder

def printInidividual():
	

def fitnessEval():
	return 0

creator.create("FMax", base.Fitness, weights = (1.0,) )
creator.create("Individual", list, fitness = creator.FMax)
toolbox = base.Toolbox()
toolbox.register("genIndividual", genInd, creator.Individual)
toolbox.register("genPop", tools.initRepeat, list, toolbox.genIndividual)
toolbox.register("evaluate", fitnessEval)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit)
toolbox.register("select", tools.selTournament, tournsize = popSize/5)
print(genInd())
