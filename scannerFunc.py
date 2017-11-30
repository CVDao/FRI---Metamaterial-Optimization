import numpy as np
from pprint import pprint

inpMatrice = np.loadtxt("output.txt", dtype= 'str', delimiter= ';')
holder = []
for i in len(range(inpMatrice[0])):
	inp = np.fromstring(inpMatrice[0][i], dtype = 'float', sep=',')
	holder.append(inp)
maxNum = 0.0
minNum = 0.0

for i in range(len(holder)):
	for j in range(len(holder[0])):
		if(holder[i][j]>maxNum):
			maxNum = holder[i][j]
		if(holder[i][j]<minNum):
			minNum = holder[i][j]
print maxNum
print minNum
