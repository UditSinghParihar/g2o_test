# Usage: python posesRead.py tf_label_opt2.txt

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

def writeG2O(X, Y, THETA):
	g2o = open('poses.g2o', 'w')
	
	for i, (x, y, theta) in enumerate(zip(X,Y,THETA)):
		line = "VERTEX_SE2 " + str(i) + " " + str(x) + " " + str(y) + " " + str(theta)
		g2o.write(line)
		g2o.write("\n")

	# Odometry
	g2o.write("# Odometry constraints")
	g2o.write("\n")
	info_mat = "500.0 0.0 0.0 500.0 0.0 500.0"
	for i in range(1, len(X)):
		p1 = (X[i-1], Y[i-1], THETA[i-1])
		p2 = (X[i], Y[i], THETA[i])
		T1_w = np.array([[math.cos(p1[2]), -math.sin(p1[2]), p1[0]], [math.sin(p1[2]), math.cos(p1[2]), p1[1]], [0, 0, 1]])
		T2_w = np.array([[math.cos(p2[2]), -math.sin(p2[2]), p2[0]], [math.sin(p2[2]), math.cos(p2[2]), p2[1]], [0, 0, 1]])
		T2_1 = np.dot(np.linalg.inv(T1_w), T2_w)
		del_x = str(T2_1[0][2])
		del_y = str(T2_1[1][2])
		del_theta = str(math.atan2(T2_1[1, 0], T2_1[0, 0]))
		
		line = "EDGE_SE2 "+str(i-1)+" "+str(i)+" "+del_x+" "+del_y+" "+del_theta+" "+info_mat
		g2o.write(line)
		g2o.write("\n")

	g2o.write("FIX 0")
	g2o.write("\n")
	g2o.close()


fig = plt.figure()
ax = plt.subplot(111)

def on_plot_hover(event):
	for line in ax.get_lines():
		if line.contains(event)[0]:
			print("Over %s node" % line.get_gid())

def draw(X, Y):
	for i in range(len(X)):
		ax.plot(X[i], Y[i], 'bo', gid=i)

	fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)

	plt.show()	


if __name__ == '__main__':
	fileName = str(argv[1])
	(X, Y, THETA, LBL) = read(fileName)

	draw(X, Y)

	writeG2O(X, Y, THETA)