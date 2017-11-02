from deap import base, creator, tools, algorithms
import numpy as np
from pprint import pprint 
import random

#200mm x 150mm
voxSize = 5  # in millimeters
padding = 5
length = 200/voxSize  #Calculates the size of the X Dimension of the array.
width = 150/voxSize   #Calculates the size of the Y dimension of the array.
#voxels assumed to be 5x5x5 mm
# a test comment
popSize = 20

#Generating the individual seems to be working correctly for now.
def genInd():
	fullHolder = []
	for i in range(0, width): #for every row
		for j in range(0, padding):
			fullHolder.append(0) #add padding 0's at the start of the col
		for k in range(0, length): # add actual randomized bits
			fullHolder.append(np.random.randint(0,2))
		for l in range(0, padding):
			fullHolder.append(0) #add padding 0's at the end of the col
	teethY = width/2
	fullHolder[(teethY+1)*length] = 1
	fullHolder[(teethY-1)*length] = 1
	return fullHolder

def printIndividual(ind): #ind is meant to be the individual, not quite sure if this is right so may need tweaking
	F = open("transFile.txt", "w+")
	F.write('%d\n' %length)
	F.write('%d\n' %width)
	for i in range(0,width):
		myString = ''
		for j in range(0, length):
			myString += str(ind[0][i*length+j])
		F.write(myString)
	F.close()

def ocxTwoPoint(ind1, ind2):
	size = min(len(ind1[0]), len(ind2[0]))
    	cxpoint1 = random.randint(1, size)
    	cxpoint2 = random.randint(1, size - 1)
    	if cxpoint2 >= cxpoint1:
    	    cxpoint2 += 1
    	else: # Swap the two cx points
    	    cxpoint1, cxpoint2 = cxpoint2, cxpoint1
   
    	ind1[0][cxpoint1:cxpoint2], ind2[0][cxpoint1:cxpoint2] \
    	    = ind2[0][cxpoint1:cxpoint2], ind1[0][cxpoint1:cxpoint2]
	return ind1, ind2
def omutFlipBit(individual, indpb):
	for i in xrange(len(individual[0])):
        	if random.random() < indpb:
      			individual[0][i] = type(individual[0][i])(not individual[0][i])
	return individual,

#run printIndividual, then call the other guys code, then eval fitness
def fitnessEval(ind):
	printIndividual(ind)
	return 0,

creator.create("FMax", base.Fitness, weights = (1.0,) )
creator.create("Individual", list, fitness = creator.FMax)
toolbox = base.Toolbox()
toolbox.register("genIndividual", tools.initRepeat, creator.Individual, genInd, n=1)
toolbox.register("genPop", tools.initRepeat, list, toolbox.genIndividual)
toolbox.register("evaluate", fitnessEval)
toolbox.register("mate", ocxTwoPoint)
toolbox.register("mutate", omutFlipBit, indpb = .05)
toolbox.register("select", tools.selTournament, tournsize = popSize/5)

finalPop = algorithms.eaSimple(toolbox.genPop(n=popSize), toolbox, 0.2, 0.3, 100)
#print(genInd())
