from sys import argv, exit
import matplotlib.pyplot as plt
import math
import numpy as np
# import os


def readKitti(fileName):
	f = open(fileName, 'r')
	A = f.readlines()
	f.close()

	X = []
	Y = []
	THETA = []

	for line in A:
		l = line.split(' ')
		
		x = float(l[3]); y = float(l[7]); theta = math.atan2(float(l[4]), float(l[0]))
		
		X.append(x)
		Y.append(y)
		THETA.append(theta)

	return (X, Y, THETA)


def draw(X, Y):
	plt.plot(X, Y, 'bo')
	plt.show()


def densify(X, Y, THETA):
	nPoses = 1389

	XD, YD, THETAD = [], [], []

	for i in range(nPoses):
		XD.append(X[i]); YD.append(Y[i]); THETAD.append(THETA[i])

		XMid = (X[i] + X[i+1])/2; YMid = (Y[i] + Y[i+1])/2; THETAMid = (THETA[i] + THETA[i+1])/2

		XD.append(XMid); YD.append(YMid); THETAD.append(THETAMid)
	# print(len(XD))

	for i in range(nPoses, len(X)):
		XD.append(X[i]); YD.append(Y[i]); THETAD.append(THETA[i])
	# print(len(XD))
	
	return XD, YD, THETAD	


def convert(X, Y, THETA):
	A = np.zeros((len(X), 12))

	for i in range(len(X)):
		T = np.identity(4)
		T[0, 3] = X[i]
		T[1, 3] = Y[i]
		R = np.array([[math.cos(THETA[i]), -math.sin(THETA[i]), 0], [math.sin(THETA[i]), math.cos(THETA[i]), 0], [0, 0, 1]])
		T[0:3, 0:3] = R
		
		A[i] = T[0:3, :].reshape(1, 12)

	return A


if __name__ == '__main__':
	(X, Y, THETA) = readKitti(argv[1])

	print(len(X), len(Y), len(THETA))
	draw(X, Y)

	XD, YD, THETAD = densify(X, Y, THETA)
	print(len(XD), len(YD), len(THETAD))
	draw(XD, YD)

	A = convert(XD, YD, THETAD)

	np.savetxt('densePose2.kitti', A, delimiter=' ')