import numpy as np

inpMatrice = np.loadtxt("output.txt", dtype= 'str', delimiter= ';')
print inpMatrice
holder = []
for i in range(len(inpMatrice)):
	inp = np.fromstring(inpMatrice[i], dtype = 'float', sep=',')
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
