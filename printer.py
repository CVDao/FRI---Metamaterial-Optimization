import matplotlib as mpl
from matplotlib import pyplot
import numpy as np

allVals = np.loadtxt("output.txt", dtype = 'str', delimiter = ';') #create matrix for y vals
yVals = []
for r in range(0, len(allVals)):
    tempHolder = []
    for c in range(0, len(allVals[0])-1):
        tempHolder2 = np.fromstring(allVals[r][c], dtype = 'float', sep=",")
        tempHolder.append(tempHolder2[2])
    yVals.append(tempHolder)
#print yVals

cmap = mpl.colors.ListedColormap(['blue','black','red'])
bounds=[-6,-1e-14, 1e-14,6]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

img = pyplot.imshow(yVals, interpolation='nearest', cmap = cmap, norm=norm)

pyplot.colorbar(img, cmap=cmap, norm=norm, boundaries = bounds, ticks = [-5,0,5])
pyplot.show()
