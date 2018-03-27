# Navigate (pray before use)

from sys import stdout, stderr
from math import sqrt, pi, cos, sin
from collections import deque, defaultdict

#UNCOMMENT# import motor
# def turn(radius, direction, pwmValue):
# def stop():
# def straight(pwmValue):
# def setDirection(direction):
###

def dummy():
	return False

import environment
# def stuff conversion and stuff
# def detect_obstacle(val):
### 

OUTSIDE = -1
UNKNOWN = 0
VISITED = 1
OBSTACLE = 2
BEACON = 7

# cross product error for straightness
CP_ERROR = 0.2

# positions of the three beacons in order (pos, init rssi)
beacons = None

discovered, rows, cols = None, None, None
vdir = None
scale = 1

# functions to calculate things
def sqr(x):
	return x*x

def dist(a, b):
	return sqrt(sqr(a[0]-b[0]) + sqr(a[1]-b[1]) + sqr(a[2]-b[2])) / scale

def cross(a, b):
	return a[0]*b[1] - a[1]*b[0]

def get_ratio(power, distance):
	return power * distance * distance

def in_grid(pos):
	return pos[0] >= 0 and pos[1] >= 0 and pos[0] < rows and pos[1] < cols

def direction(s, t):
	x, y = t[0]-s[0], t[1]-s[1]
	norm = sqrt(sqr(x) + sqr(y))
	return (float(x)/norm, float(y)/norm)

# TODO actually use the motor library
# move robot from cur to goal following a straight line
def move_to(cur, goal):
	global vdir
	stderr.write("move from " + str(cur) + " to " + str(goal) + '\n')
	# left, straight, right ?
	aim = direction(cur, goal)
	cross_prod = cross(vdir, aim)
	stderr.write("cross: " + str(cross_prod) + '\n')
	if cross_prod > CP_ERROR:
		# turn left
		stderr.write("turn left\n\n")
	elif cross_prod < -CP_ERROR:
		# turn right
		stderr.write("turn right\n\n")
	else:
		# straight
		stderr.write("straight\n\n")
	# TODO change this
	vdir = direction(cur, goal)
	return goal

# follow path from current position to goal
def follow_path(pos, path, grid):
	stderr.write("PATH: " + str(path) + '\n\n')
	for cell in path:
		pos = move_to(pos, cell)
	stderr.write("done path ~~~ \n\n")
	return pos

# find next unvisited grid cell
def reachable(pos, grid):
	todo = deque()
	vis = set()
	previous = dict()
	goal = None

	# do a bfs
	cur = tuple(pos[0:2])
	todo.append(cur)
	vis.add(cur)

	while todo:
		cur = todo.popleft()
		if grid[cur[0]][cur[1]] == UNKNOWN:
			goal = cur
			break
		for nbr in [
				tuple([cur[0], cur[1]+1]),
				tuple([cur[0], cur[1]-1]),
				tuple([cur[0]+1, cur[1]]),
				tuple([cur[0]-1, cur[1]])
				]:
			if in_grid(nbr) and grid[nbr[0]][nbr[1]] != OBSTACLE and nbr not in vis:
				todo.append(nbr)
				previous[nbr] = cur
				vis.add(nbr)

	# no unvisited cells left, return None
	if goal is None:
		return None

	# find path to next unvisited cell, follow it
	path = []
	while goal in previous:
		path.append(goal)
		goal = previous[goal]
	pos = follow_path(pos, path[::-1], grid)
	return pos

# detect obstacles, find neighbour
def get_neighbour(pos, grid):
	best = -2
	aim = -1
	for i in range(0, 4):
		dot_p = vdir[0] * cos(i*pi/2) + vdir[1] * sin(i*pi/2)
		if dot_p > best:
			best = dot_p
			aim = i

	# start with left
	left = (aim + 3) % 4
	possible = None
	stderr.write(" @ " + str(pos) + '\n')
	# we do not need to check behind the robot
	for i in range(0, 3):
		cur = (left + i) % 4
		to_check = (int(round(pos[0] + cos(cur*pi/2))), int(round(pos[1] + sin(cur*pi/2))))
		stderr.write("TRY " + str(to_check) + '\n')
		# check to see if we want to go there
		if grid[to_check[0]][to_check[1]] == UNKNOWN:
			# check to see if we can go there
			blocked = environment.detect_obstacle(i-1)
			if blocked:
				grid[to_check[0]][to_check[1]] = OBSTACLE
			elif possible is None:
				possible = to_check
	stderr.write("neighbour from " + str(pos) + " : " + str(possible) + '\n')
	return possible

# explore unvisited area by following the right edge
def explore(pos, grid):
	global rows, cols, scale, discovered
	grid[pos[0]][pos[1]] = VISITED
	next_pos = get_neighbour(pos, grid)
	while next_pos is not None:
		pos = move_to(pos, next_pos)
		grid[pos[0]][pos[1]] = VISITED
		next_pos = get_neighbour(pos, grid)
	return pos

# assume the input has been cleaned up
# positions of the three beacons in order (pos, init rssi)
# initial position of robot (pair)
# to_search (visited array)
def search(init_beacons, robot, init_dir, to_search, sc):
	global scale, rows, cols, discovered, vdir, beacons
	discovered = 0
	rows = len(to_search)
	cols = len(to_search[0])
	scale = sc
	beacons = init_beacons
	vdir = init_dir

	# initialize beacon dist
	for i in range(0, 3):
		to_search[beacons[i][0][0]][beacons[i][0][1]] = BEACON
		beacons[i].append(get_ratio(beacons[i][1], dist(robot, beacons[i][0])))

	# debug
	stderr.write("scale: " + str(scale) + '\n')
	stderr.write("init beacons: \n" + '\n'.join(map(str, beacons)) + '\n')
	stderr.write("init robot: " + str(robot) + '\n')
	stderr.write("init dir: " + str(vdir) + '\n')
	stderr.write("to_search: \n" + '\n'.join(map(str, to_search)) + '\n')
	stderr.write("END INITIAL DEBUG\n\n")

	# do the search
	robot = reachable(robot, to_search)
	while robot is not None:
		stderr.write("explore from " + str(robot) + ' ------------------ \n\n')
		robot = explore(robot, to_search)
		stderr.write("to_search: \n" + '\n'.join(map(str, to_search)) + '\n\n')
		robot = reachable(robot, to_search)

	return discovered

