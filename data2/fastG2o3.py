from sys import argv, exit
import matplotlib.pyplot as plt
import math
import numpy as np


def read(fileName):
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
		LBL.append(int(lbl.rstrip('\n')))

	return (X, Y, THETA, LBL)


def drawTheta(X, Y, LBL, thetas):
	ax = plt.subplot(111)

	X0 = []; Y0 = []; X1 = []; Y1 = []; X2 = []; Y2 =[]; X3 = []; Y3 = [];
	
	for i in range(len(LBL)):

		x2 = math.cos(thetas[i]) + X[i]
		y2 = math.sin(thetas[i]) + Y[i]
		plt.plot([X[i], x2], [Y[i], y2], 'm->')

		if LBL[i] == 0:
			X0.append(X[i])
			Y0.append(Y[i])

		elif LBL[i] == 1:
			X1.append(X[i])
			Y1.append(Y[i])

		elif LBL[i] == 2:
			X2.append(X[i])
			Y2.append(Y[i])

		elif LBL[i] == 3:
			X3.append(X[i])
			Y3.append(Y[i])

	ax.plot(X0, Y0, 'ro', label='Rackspace', zorder = 2)
	ax.plot(X1, Y1, 'bo', label='Corridor', zorder = 4)
	ax.plot(X2, Y2, 'go', label='Trisection', zorder = 6)
	ax.plot(X3, Y3, 'yo', label='Intersection', zorder = 8)

	plt.plot(X, Y, 'k-')

	plt.show()


def draw(X, Y, LBL):
	X0 = []; Y0 = []; X1 = []; Y1 = []; X2 = []; Y2 =[]; X3 = []; Y3 = [];
	
	for i in xrange(len(LBL)):
		if LBL[i] == 0:
			X0.append(X[i])
			Y0.append(Y[i])

		elif LBL[i] == 1:
			X1.append(X[i])
			Y1.append(Y[i])

		elif LBL[i] == 2:
			X2.append(X[i])
			Y2.append(Y[i])

		elif LBL[i] == 3:
			X3.append(X[i])
			Y3.append(Y[i])

	fig = plt.figure()
	ax = plt.subplot(111)

	ax.plot(X0, Y0, 'ro', label='Rackspace')
	ax.plot(X1, Y1, 'bo', label='Corridor')
	ax.plot(X2, Y2, 'go', label='Trisection')
	ax.plot(X3, Y3, 'yo', label='Intersection')
	plt.plot(X, Y, 'k-')

	plt.show()


if __name__ == '__main__':
	fileName = str(argv[1])
	(X, Y, THETA, LBL) = read(fileName)

	# drawTheta(X, Y, LBL, THETA)