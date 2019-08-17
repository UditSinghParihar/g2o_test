from sys import argv, exit
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import stats

def read(fileName):
	f = open(fileName, 'r')
	A = f.readlines()
	f.close()

	X = []
	Y = []
	LBL = []

	for line in A:
		(x, y, theta, lbl) = line.split(' ')
		X.append(float(x))
		Y.append(float(y))
		LBL.append(int(lbl.rstrip('\n')))

	X_temp = X
	Y_temp = Y
	X = [-y for y in Y_temp]
	Y = [x for x in X_temp]

	return (X, Y, LBL)


def calcTheta(x1, x2, y1, y2):
	if(x2 == x1):
		if(y2 > y1):
			theta = math.pi/2
		else:
			theta = 3*math.pi/2
	else:
		theta = math.atan((y2-y1)/(x2-x1))

	if(x2-x1 < 0):
		theta += math.pi

	return theta


def blueFix(st, end, X, Y, LBL, Node_meta):
	Thetas = []; mid = st + (end - st)/2

	xMid = 0; yMid =0; fill = True

	for i in xrange(st, end-9):
		X1 = [X[j] for j in xrange(i, i+5)]; Y1 = [Y[j] for j in xrange(i, i+5)] 
		X2 = [X[j] for j in xrange(i+5, i+10)]; Y2 = [Y[j] for j in xrange(i+5, i+10)]

		(m1, c1, _, _, _) = stats.linregress(X1, Y1)
		(m2, c2, _, _, _) = stats.linregress(X2, Y2)

		dm1 = math.degrees(math.atan(m1)); dm2 = math.degrees(math.atan(m2))
		delTheta = dm1 - dm2
		# print(delTheta, dm1, dm2)

		if(delTheta > 70 and delTheta < 110 and fill):
			xMid = X2[0]; yMid = Y2[0]
			Node_meta.append((X[st], Y[st], xMid, yMid, LBL[mid]))
			Node_meta.append((xMid, yMid, X[end], Y[end], LBL[mid]))
			fill = False

		# x1s = X1[0]; x1e = X1[-1] 
		# y1s = m1*x1s + c1; y1e = m1*x1e + c1
		# x2s = X2[0]; x2e = X2[-1]
		# y2s = m2*x2s + c2; y2e = m2*x2e + c2

		# ax = plt.subplot(1,1,1)
		# ax.plot([x1s, x1e], [y1s, y1e], 'r-')
		# ax.plot([x2s, x2e], [y2s, y2e], 'g-')
		# ax.plot(X[st:end], Y[st:end], 'bo')
		# ax.plot(X1, Y1, 'ro')
		# ax.plot(X2, Y2, 'go')
		# plt.show()

	if(fill == True):
		Node_meta.append((X[st], Y[st], X[end], Y[end], LBL[mid]))

	# ax = plt.subplot(1,1,1)
	# ax.plot(X[st:end], Y[st:end], 'bo')
	# ax.plot(xMid, yMid, 'ro')
	# # plt.xlim(-5, 25)
	# # plt.ylim(-15, 15)
	# plt.show()
	# print("Inside blueFix--------")



def meta(X, Y, LBL):
	Node_meta = []
	st = end = 0

	for i in xrange(1, len(LBL)):
		if LBL[i] == LBL[i-1]:
			end = i
			continue

		mid = st + (end - st)/2
		
		if (LBL[mid] == 1):
			blueFix(st, end, X, Y, LBL, Node_meta)

		# else:
		Node_meta.append((X[st], Y[st], X[end], Y[end], LBL[mid]))
	
		st = end + 1
		end = st
	return Node_meta


def drawManh(Nodes):
	ax = plt.subplot(1,1,1)

	for line in Nodes:
		lbl = line[4]
		x = [line[0], line[2]]
		y = [line[1], line[3]]

		if lbl == 0:
			ax.plot(x, y, 'ro')
			ax.plot(x, y, 'r-')

		elif lbl == 1:
			ax.plot(x, y, 'bo')
			ax.plot(x, y, 'b-')

		elif lbl == 2:
			ax.plot(x, y, 'go')
			ax.plot(x, y, 'g-')

		elif lbl == 3:
			ax.plot(x, y, 'yo')
			ax.plot(x, y, 'y-')

	# plt.xlim(-2, 28)
	# plt.ylim(-15, 15)
	plt.show()


def drawTheta(Node_meta, thetas):
	ax = plt.subplot(1,1,1)

	i = 0
	for line in Node_meta:
		
		lbl = line[4]
		x = [line[0], line[2]]
		y = [line[1], line[3]]

		x2 = math.cos(thetas[i]) + x[0]
		y2 = math.sin(thetas[i]) + y[0]
		# plt.plot([x[0], x2], [y[0], y2], 'm->')

		if lbl == 0:
			ax.plot(x, y, 'ro')
			ax.plot(x, y, 'r-')

		elif lbl == 1:
			ax.plot(x, y, 'bo')
			ax.plot(x, y, 'b-')

		elif lbl == 2:
			ax.plot(x, y, 'go')
			ax.plot(x, y, 'g-')

		elif lbl == 3:
			ax.plot(x, y, 'yo')
			ax.plot(x, y, 'y-')

		i = i+1

	# plt.xlim(-5, 25)
	# plt.ylim(-15, 15)
	plt.show()


def outRemove(Node_meta):
	i = 0; Nodes = []

	while (i < len(Node_meta)):
		line = Node_meta[i]
		lbl = line[4]
		x = [line[0], line[2]]
		y = [line[1], line[3]]

		leng = ((x[0]-x[1])**2 + (y[0]-y[1])**2)**(0.5)
		if(leng < 0.1):
			if(Node_meta[i-1][4] == Node_meta[i+1][4]):
				newNode = (Node_meta[i-1][0], Node_meta[i-1][1], Node_meta[i+1][2], Node_meta[i+1][3], Node_meta[i-1][4])
				Nodes.pop()
				Nodes.append(newNode)
				i = i+1

		else:
			Nodes.append(line)
		
		i = i+1

	return Nodes


def manh(Node_meta, thetas):
	Nodes = []; accTheta = 0; Thetas = []
	line = Node_meta[0]
	x = [line[0], line[2]]; y = [line[1], line[3]]
	leng = ((x[0]-x[1])**2 + (y[0]-y[1])**2)**(0.5)

	Nodes.append((leng, accTheta, line[4]))
	# print("Total theta: ", accTheta, "Length: ", leng)

	for i in xrange(1, len(Node_meta)):
		line = Node_meta[i]
		x = [line[0], line[2]]; y = [line[1], line[3]]
		leng = ((x[0]-x[1])**2 + (y[0]-y[1])**2)**(0.5)

		delTheta = math.degrees(thetas[i]-thetas[i-1])

		binTheta = 0
		if(delTheta > -20 and delTheta < 20):
			binTheta = 0
		elif((delTheta > 160 and delTheta < 200) or (delTheta < -160 and delTheta > -200)):
			binTheta = 180
		elif(delTheta > 20 and delTheta < 160):
			binTheta = 90
		elif(delTheta < -200):
			binTheta = 90
		elif(delTheta < -75 and delTheta > -105):
			binTheta = -90

		accTheta += binTheta
		Nodes.append((leng, accTheta, line[4]))
		# print("Delta theta: ", delTheta, "Binned to: ", binTheta, "Total theta: ", accTheta, "Length: ", leng)

	return Nodes


def extManh(Nodes_manh):
	Nodes = []; i = 0

	l1 = 0; b1 = 0; l2 = 0; b2 = 0
	for line in Nodes_manh:
		mag = line[0]; theta = line[1]; lbl = line[2]
		
		if((theta - Nodes_manh[i-1][1] == 180) and (i != 0)):
			l1 = l2 - 0.2
			b1 = b2 + 0.2
			l2 = l1 + mag*math.cos(math.radians(theta))
			b2 = b1 + mag*math.sin(math.radians(theta))
			Nodes.append((l1, b1, l2, b2, lbl))

		else:
			l1 = l2 
			b1 = b2
			l2 = l1 + mag*math.cos(math.radians(theta))
			b2 = b1 + mag*math.sin(math.radians(theta))

			Nodes.append((l1, b1, l2, b2, lbl))

		i = i+1

	return Nodes

if __name__ == '__main__':
	fileName = str(argv[1])
	(X, Y, LBL) = read(fileName)

	# X = X[450:-1]; Y = Y[450:-1]; LBL = LBL[450:-1]
	# print("Length: ", len(X))
	
	Node_meta = meta(X, Y, LBL)
	print(len(Node_meta))
	Node_meta = Node_meta[7:200];
	# exit(1)

	Node_meta = outRemove(Node_meta)

	Nodes = []

	thetas = []
	for line in Node_meta:
		lbl = line[4]
		x = [line[0], line[2]]
		y = [line[1], line[3]]

		theta = calcTheta(x[0], x[1], y[0], y[1])
		thetas.append(theta)

	drawTheta(Node_meta, thetas)
	
	Nodes_manh = manh(Node_meta, thetas)
	Nodes = extManh(Nodes_manh)
	drawManh(Nodes)

	# for line in Nodes:
	# 	print(line)

	poses = open("mlp_in.txt", 'w')
	for line in Nodes:
		info = str(line[0])+" "+str(line[1])+" "+ str(line[2])+" "+ str(line[3])+" "+ str(line[4]) 
		poses.write(info)
		poses.write("\n")

	poses.close()
	