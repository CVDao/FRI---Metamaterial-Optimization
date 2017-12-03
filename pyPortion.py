from deap import base, creator, tools, algorithms
import numpy as np
from pprint import pprint 
import random
import subprocess

#200mm x 150mm
voxSize = 5  # in millimeters
padding = 4
width =  10#150/voxSize   #Calculates the size of the Y dimension of the array. I.e. The Rows
length = 14#200/voxSize  #Calculates the size of the X Dimension of the array. I.e. the Columns
lp = length + 2*padding
handleSize = 5
teethSize = 4
teethGap = 1
popSize = 5
genSize = 1
teethY = width/2
testString = [[0,0,1,1,0,0,0,0,0,0,1,1]]

def genInd():
	fullHolder = []
	for i in range(0, width): #for every row
		for k in range(0, length): # add actual randomized bits
			fullHolder.append(np.random.randint(0,2))
	return fullHolder

def printIndividual(ind): #ind is meant to be the individual, not quite sure if this is right so may need tweaking
    	fullHolder = []
    	for i in range(0, width): #for every row
    	    	for j in range(0, padding):
			fullHolder.append(0) #add padding 0's at the start of the col
    	    	for k in range(0, length): # add actual randomized bits
			fullHolder.append(ind[0][i*length + k])
    	    	for l in range(0, padding):
			fullHolder.append(0) #add padding 0's at the end of the col
	for i in range(1, teethSize+1):
		 fullHolder[(teethY+teethGap)*(length+2*padding)-i] = 1 #teeth first set
		 fullHolder[(teethY-teethGap)*(length+2*padding)-i] = 1

	for i in range(0,handleSize):
		fullHolder[i] = 1
		fullHolder[(width-1)*(length+2*padding)+i] = 1

	#post process section
	myQueue = [(0,0), (width-1,0), (teethY+teethGap,lp-teethSize), (teethY-teethGap, lp-teethSize) ]
	Connecteds = []
	while(len(myQueue) != 0):
		operator = myQueue.pop()
		Connecteds.append(operator)
		if(operator[0]-1 >= 0):
			if(fullHolder[(operator[0]-1)*lp + operator[1]] == 1):
				if ((operator[0]-1, operator[1]) not in Connecteds):
					myQueue.append((operator[0]-1, operator[1]))
		if(operator[1]+1 < lp):
			if(fullHolder[(operator[0])*lp + operator[1]+1] == 1):
				if ((operator[0], operator[1]+1) not in Connecteds):
					myQueue.append((operator[0], operator[1] + 1))
		if(operator[0]+1 < width):
			if(fullHolder[(operator[0]+1)*lp + operator[1]] == 1):
				if ((operator[0]+1, operator[1]) not in Connecteds):
					myQueue.append((operator[0]+1, operator[1]))
		if(operator[1]-1 >= 0):
			if(fullHolder[(operator[0])*lp + operator[1]-1] == 1):
				if ((operator[0], operator[1]-1) not in Connecteds):
					myQueue.append((operator[0], operator[1] - 1))

		if(operator[0]-1 >= 0 & operator[1] + 1 <lp):
			if(fullHolder[(operator[0]-1)*lp + operator[1] +1] == 1):
				fullHolder[(operator[0]-1)*lp + operator[1]] = 1
				fullHolder[(operator[0])*lp + operator[1]+1] = 1
				Connecteds.append((operator[0]-1, operator[1]))
				Connecteds.append((operator[0], operator[1]+1))

		if(operator[0]+1 < width & operator[1] + 1 <lp):
			if(fullHolder[(operator[0]+1)*lp + operator[1] +1] == 1):
				fullHolder[(operator[0]+1)*lp + operator[1]] = 1
				fullHolder[(operator[0])*lp + operator[1]+1] = 1
				Connecteds.append((operator[0]+1, operator[1]))
				Connecteds.append((operator[0], operator[1]+1))
	for i in range(width):
		for j in range(lp):
			if((i,j) not in Connecteds):
				fullHolder[i*lp + j] = 0
	for i in range(1, teethSize+1):
		fullHolder[(teethY)*lp-i] = 0
	#printing section
	F = open("transFile.txt", "w+")
	F.write('%d\n' %width)
	F.write('%d\n' %lp)
	F.write('%d\n' %handleSize)
	for i in range(0,width):
		myString = ''
		for j in range(0, (length+padding+padding)):
			myString += str(fullHolder[i*(length+padding+padding)+j])
		myString += "\n"
		F.write(myString)
	for i in range(0, teethSize):
		F.write('%d %d %d %d %d\n' %(0, i, 20, 20, 20))
	F.close()

def nonFormatPrint(ind):
	F = open("unform.txt", "w+")
	F.write('%d\n' %length)
	F.write('%d\n' %width)
	for i in range(0,width):
		myString = ''
		for j in range(0, (length)):
			myString += str(ind[0][i*(length)+j])
			myString += " "
		myString += "\n"
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

def omutFlipBit(ind, indpb):
	for i in xrange(len(ind[0])):
		if random.random() < indpb:
			for j in range (2):
				if(j*lp+i < len(ind[0])):
					ind[0][j*lp+i] = type(ind[0][j*lp+i])(not ind[0][j*lp+i])
				if(i-j*lp >= 0):
					ind[0][i-j*lp] = type(ind[0][i-j*lp])(not ind[0][i-j*lp])
	return ind,

def myMapper(ind, inpMatrice):
	holder = [] # holds all total time step matrices
	for i in range(1000):
		onesCounter = 0
		tempMatrice = [] # holds the single timestep matrix
		for j in range(width): # row
			tempRow = []
			for k in range(padding):
				tempRow.append([0,0,0])
			for k in range(length): # column order
				if(ind[0][j*length + j] == 1):
					tempInp = np.fromstring(inpMatrice[i][onesCounter], dtype = 'float', sep=',')
					onesCounter = onesCounter + 1
					tempRow.append(tempInp)
				else:
					tempRow.append([0,0,0])
			for k in range(padding):
				tempRow.append([0,0,0])

			if(j == teethY+teethGap | teethY-teethGap):
				for l in range(1, teethSize+1):
					tempRow[lp-l] = np.fromstring(inpMatrice[i][onesCounter], dtype = 'float', sep=',')
					onesCounter = onesCounter + 1
				
			tempMatrice.append(tempRow)
		holder.append(tempMatrice)
	return holder

#run printIndividual, then call the other guys code, then eval fitness
def fitnessEval(ind):
	printIndividual(ind)
	subprocess.call("./VoxCad_Test < transFile.txt > output.txt", shell = True); 
	inpMatrice = np.loadtxt("output.txt", dtype='str', delimiter=';') #inp[row][voxel] then requires extra parsing to parse string
	holder = myMapper(ind, inpMatrice)

	oD = holder[0][teethY+teethGap][lp-1][1] # original distance
	maxD = 0
	minUT = 1000
	maxUT = 0

	for i in range(1000):
		val = holder[i][teethY+teethGap][lp-1][1]
	#	if(val < minD):
	#		minBT = val
		if(val > maxD):
			maxD = val
	print maxD - oD
	return maxD- oD,

creator.create("FMax", base.Fitness, weights = (1.0,) )
creator.create("Individual", list, fitness = creator.FMax)
toolbox = base.Toolbox()
toolbox.register("genIndividual", tools.initRepeat, creator.Individual, genInd, n=1) #n should always be set to one.
toolbox.register("genPop", tools.initRepeat, list, toolbox.genIndividual)
toolbox.register("evaluate", fitnessEval)
toolbox.register("mate", ocxTwoPoint)
toolbox.register("mutate", omutFlipBit, indpb = .05)
toolbox.register("select", tools.selTournament, tournsize = popSize/5)

finalPop = algorithms.eaSimple(toolbox.genPop(n=popSize), toolbox, 0.2, 0.3, genSize)
best =  tools.selBest(finalPop[0], 1)
printIndividual(best[0])
