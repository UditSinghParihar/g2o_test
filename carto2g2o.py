from sys import argv, exit
import matplotlib.pyplot as plt
import math
import numpy as np

def getTheta(X ,Y):
	THETA = [None]*len(X)
	for i in xrange(1, len(X)-1):
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
		LBL.append(float(lbl.rstrip('\n')))

	X_temp = X
	Y_temp = Y
	X = [-y for y in Y_temp]
	Y = [x for x in X_temp]

	THETA = getTheta(X, Y)

	return (X, Y, THETA, LBL)

def meta(X, Y, THETA, LBL):
	X_meta = []
	Y_meta = []
	THETA_meta = []
	st = end = 0

	for i in xrange(1, len(LBL)):
		if LBL[i] == LBL[i-1]:
			end = i
			continue

		mid = st + (end - st)/2
		X_meta.append(X[mid])
		Y_meta.append(Y[mid])
		THETA_meta.append(THETA[mid])

		st = end + 1
		end = st
	return (X_meta, Y_meta, THETA_meta)

def writeG2O(X_meta,Y_meta,THETA_meta):
	g2o = open("poses.g2o", 'w')
	for i, (x, y, theta) in enumerate(zip(X_meta,Y_meta,THETA_meta)):
		line = "VERTEX_SE2 " + str(i) + " " + str(x) + " " + str(y) + " " + str(theta)
		g2o.write(line)
		g2o.write("\n")

	info_mat = "500.0 0.0 0.0 500.0 0.0 500.0"
	for i in xrange(1, len(X_meta)):
		p1 = (X_meta[i-1], Y_meta[i-1], THETA_meta[i-1])
		p2 = (X_meta[i], Y_meta[i], THETA_meta[i])
		T1_w = np.array([[math.cos(p1[2]), -math.sin(p1[2]), p1[0]], [math.sin(p1[2]), math.cos(p1[2]), p1[1]], [0, 0, 1]])
		T2_w = np.array([[math.cos(p2[2]), -math.sin(p2[2]), p2[0]], [math.sin(p2[2]), math.cos(p2[2]), p2[1]], [0, 0, 1]])
		T2_1 = np.dot(np.linalg.inv(T1_w), T2_w)
		del_x = str(T2_1[0][2])
		del_y = str(T2_1[1][2])
		del_theta = str(np.arccos(T2_1[0][0]))
		
		line = "EDGE_SE2 "+str(i-1)+" "+str(i)+" "+del_x+" "+del_y+" "+del_theta+" "+info_mat
		g2o.write(line)
		g2o.write("\n")


	e1 = (8, 12); e2 = (9, 11)
	e3 = (17, 31); e4 = (18, 30); e5 = (19, 29); e6 = (22, 26)
	# e7 = (33, 57); e8 = (39, 48)
	edges = [e1, e2, e3, e4, e5, e6]

	info_mat = "200.0 0.0 0.0 1000.0 0.0 1000.0"
	for e in edges:
		p1 = (X_meta[e[0]], Y_meta[e[0]], THETA_meta[e[0]])
		p2 = (X_meta[e[1]], Y_meta[e[1]], THETA_meta[e[1]])
		T1_w = np.array([[math.cos(p1[2]), -math.sin(p1[2]), p1[0]], [math.sin(p1[2]), math.cos(p1[2]), p1[1]], [0, 0, 1]])
		T2_w = np.array([[math.cos(p2[2]), -math.sin(p2[2]), p2[0]], [math.sin(p2[2]), math.cos(p2[2]), p2[1]], [0, 0, 1]])
		T2_1 = np.dot(np.linalg.inv(T1_w), T2_w)
		del_x = str(T2_1[0][2])
		del_y = str(0)
		del_theta = str(math.pi)
		line = "EDGE_SE2 "+str(e[0])+" "+str(e[1])+" "+del_x+" "+del_y+" "+del_theta+" "+info_mat
		g2o.write(line)
		g2o.write("\n")

	corWidth = 1.789
	edges = [(9, 23), (8, 21), (7, 17)]

	info_mat = "200.0 0.0 0.0 1000.0 0.0 1000.0"
	for e in edges:
		p1 = (X_meta[e[0]], Y_meta[e[0]], THETA_meta[e[0]])
		p2 = (X_meta[e[1]], Y_meta[e[1]], THETA_meta[e[1]])
		T1_w = np.array([[math.cos(p1[2]), -math.sin(p1[2]), p1[0]], [math.sin(p1[2]), math.cos(p1[2]), p1[1]], [0, 0, 1]])
		T2_w = np.array([[math.cos(p2[2]), -math.sin(p2[2]), p2[0]], [math.sin(p2[2]), math.cos(p2[2]), p2[1]], [0, 0, 1]])
		T2_1 = np.dot(np.linalg.inv(T1_w), T2_w)
		del_x = str(T2_1[0][2])
		del_y = str(-corWidth)
		del_theta = str(0)
		line = "EDGE_SE2 "+str(e[0])+" "+str(e[1])+" "+del_x+" "+del_y+" "+del_theta+" "+info_mat
		g2o.write(line)
		g2o.write("\n")

	g2o.write("FIX 0")
	g2o.write("\n")
	g2o.close()	

if __name__ == '__main__':
	fileName = str(argv[1])
	(X, Y, THETA, LBL) = read(fileName)

	(X_meta, Y_meta, THETA_meta) = meta(X, Y, THETA, LBL)

	X = X[0:500]; Y = Y[0:500]
	X_meta = X_meta[0:33]; Y_meta = Y_meta[0:33]; THETA_meta = THETA_meta[0:33]

	writeG2O(X_meta,Y_meta,THETA_meta)

	plt.plot(X_meta, Y_meta, 'bo')
	plt.plot(X_meta, Y_meta, 'k')

	for i in xrange(len(X_meta)):
		x2 = math.cos(THETA_meta[i]) + X_meta[i]
		y2 = math.sin(THETA_meta[i]) + Y_meta[i]
		plt.plot([X_meta[i], x2], [Y_meta[i], y2], 'r->')
	
	# plt.plot(X, Y, 'bo')
	# plt.plot(X_meta[17], Y_meta[17], 'ro')
	# plt.plot(X_meta[7], Y_meta[7], 'ro')
	# plt.plot(X_meta[39], Y_meta[39], 'ro')
	# plt.plot(X_meta[48], Y_meta[48], 'ro')
	plt.xlim(-5, 25)
	plt.ylim(-15, 15)
	plt.show()

