from sys import argv, exit
import matplotlib.pyplot as plt


def read(fileName):
	f = open(fileName, 'r')
	A = f.readlines()
	f.close()

	Node_meta = []

	for line in A:
		(l1, b1, l2, b2, lbl) = line.split(' ')
		Node_meta.append((float(l1), float(b1), float(l2), float(b2), float(lbl.rstrip('\n'))))

	return Node_meta

def drawNode(Node_meta):
	ax = plt.subplot(1,1,1)

	for line in Node_meta:
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

	# plt.xlim(-30, 45)
	# plt.ylim(-50, 25)
	plt.show()


if __name__ == '__main__':
	fileName = str(argv[1])
	Node_meta = read(fileName)

	# Using half trajectory
	# Node_meta = Node_meta[0:33]

	drawNode(Node_meta)