import matplotlib.pyplot as plt
from sys import argv
import csv
import math


def getTheta(X ,Y):
	THETA = [None]*len(X)
	for i in range(1, len(X)-1):
		if(X[i+1] == X[i-1]):
			if (Y[i+1]>Y[i-1]):
				THETA[i] = math.pi/2
			else:
				THETA[i] = 3*math.pi/2
			continue

		THETA[i] = math.atan((Y[i+1]-Y[i-1])/(X[i+1]-X[i-1]))

		if(X[i+1]-X[i-1] < 0):
			THETA[i] += math.pi 

	if X[1]==X[0]:
		if Y[1] > Y[0]:
			THETA[0] = math.pi/2
		else:
			THETA[0] = 3*math.pi/2
	else:
		THETA[0] = math.atan((Y[1]-Y[0])/(X[1]-X[0]))

	if X[-1] == X[len(Y)-2]:
		if Y[1] > Y[0]:
			THETA[-1] = math.pi/2
		else:
			THETA[-1] = 3*math.pi/2
	else:
		THETA[-1] = math.atan((Y[-1]-Y[len(Y)-2])/(X[-1]-X[len(Y)-2]))

	return THETA


def readCsv(fileName):
	X = []
	Y = []
	THETA = []
	LBL = []

	with open(fileName, 'rt') as f:
		A = csv.reader(f)


		for idx, line in enumerate(A):
			if(idx == 0):
				continue
			else:
				X.append(float(line[1]))
				Y.append(float(line[2]))
				# THETA.append(float(line[3]))
				LBL.append(float(line[4]))

	X_temp = X
	Y_temp = Y
	X = [-y for y in Y_temp]
	Y = [x for x in X_temp]

	THETA = getTheta(X, Y)

	return (X, Y, THETA, LBL)


def readG2o(fileName):
	f = open(fileName, 'r')
	A = f.readlines()
	f.close()

	X = []
	Y = []
	THETA = []

	for line in A:
		if "VERTEX_SE2" in line:
			(ver, ind, x, y, theta) = line.split(' ')
			X.append(float(x))
			Y.append(float(y))
			THETA.append(float(theta.rstrip('\n')))

	return (X, Y, THETA)

def readTxt(fileName):
	f = open(fileName, 'r')
	A = f.readlines()
	f.close()

	X = []
	Y = []
	THETA = []
	LBL = []

	for line in A:
		(x, y, theta, lbl) = line.split(' ')
		X.append(float(x))
		Y.append(float(y))
		THETA.append(float(theta))
		LBL.append(float(lbl.rstrip('\n')))

	X_temp = X
	Y_temp = Y
	X = [-y for y in Y_temp]
	Y = [x for x in X_temp]

	return (X, Y, THETA, LBL)


def draw(X1, Y1, X2, Y2, X3, Y3, noisy=True, opt=True ,gt=True):
	if(opt == True):
		plt.plot(X1, Y1, 'r-', markersize=5, linewidth=2 ,label='Optimized')
	
	if(noisy == True):
		plt.plot(X2, Y2, 'b-', markersize=5, linewidth=2, label='Noisy')
	
	if(gt == True):
		plt.plot(X3, Y3, 'g-', markersize=5, linewidth=2 ,label='Ground Truth')
	
	plt.legend()
	plt.show()


if __name__ == '__main__':
	fileG2o = str(argv[1])
	fileCsv = str(argv[2])
	fileTxt = str(argv[3])
	
	(X1, Y1, THETA1) =	readG2o(fileG2o)

	(X2, Y2, THETA2, LBL) = readCsv(fileCsv)

	(X3, Y3, THETA3, LBL) = readTxt(fileTxt)	

	draw(X1, Y1, X2, Y2, X3, Y3, opt=False)
	draw(X1, Y1, X2, Y2, X3, Y3, noisy=False, gt=False)
	draw(X1, Y1, X2, Y2, X3, Y3)
	draw(X1, Y1, X2, Y2, X3, Y3, noisy=False)