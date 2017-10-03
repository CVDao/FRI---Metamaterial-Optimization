from deap import base, creator, tools, algorithms
import numpy

#200mm x 150mm
length = 40
width = 30
#voxels assumed to be 5x5x5 mm

popSize = 20


def main():
	creator.create("FMax", base.Fitness, weights = (1.0,) )
	creator.create("Individual", list, fitness = creator.FMax)
	toolbox = base.Toolbox()
	pop = toolbox.population(n = popSize)
 
