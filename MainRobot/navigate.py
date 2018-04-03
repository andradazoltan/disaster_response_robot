import robot
from manual import *
from sys import stdout, stderr
from math import sqrt, pi, cos, sin, asin, acos
from collections import deque, namedtuple

from motor import cleanup, stop

Circle = namedtuple("Circle", "x y r")

# communication and sensors
###

########################################################################

# grid values
OUTSIDE = -1
UNKNOWN = 0
VISITED = 1
OBSTACLE = 2
OBJECT = 3

# epsilons and errors
ANG_ROTATE = 50
ANG_ERROR = 10
DIST_ERROR = 0.368
EPS = 1e-3

# grid info
discovered, rows, cols = None, None, None
scale = 1.0

# mode info
mode = robot.AUTO

# robot info
prev_pos, vdir = None, None
robot_id = None

########################################################################

# square function
def sqr(x):
	return x*x

# distance function
def dist(a, b):
	norm = 0
	for i in range(0, min(len(a), len(b))):
		norm += sqr(a[i]-b[i])
	return sqrt(norm)

# cross product
def cross(a, b):
	return a[0]*b[1] - a[1]*b[0]

# dot product
def dot_prod(a, b):
	return a[0]*b[0] + a[1]*b[1]

# check if pos is in grid
def in_grid(pos):
	return pos[0] >= 0 and pos[1] >= 0 and pos[0] < rows and pos[1] < cols

# get unit direction vector from s to t
def direction(s, t):
	x, y = t[0]-s[0], t[1]-s[1]
	norm = sqrt(sqr(x) + sqr(y))
	return (float(x)/norm, float(y)/norm)

########################################################################

# move robot from cur to goal
def move_to(cur, goal):
	global vdir, mode
	robot.update_cell(robot_id, cur, 'visited')

	stderr.write("move from " + str(cur) + " to " + str(goal) + '\n')

	# left, straight, right ?
	aim = direction(cur, goal)

	# get angle in degrees
	angle = asin(cross(vdir, aim)) * 180.0 / pi
	# check if this angle is obtuse
	if dot_prod(vdir, aim) < 0:
		angle = 180 - angle

	# rotate to correct direction
	if angle > EPS:
		robot.rotate(angle)

	# move to next cell
	robot.straight()

	# update vdir
	vdir = direction(cur, goal)

	# get auto / manual
	mode = robot.get_mode(robot_id)

	# update robot
	robot.update_robot(robot_id, goal, vdir)
	robot.update_cell(robot_id, goal, 'robot')

	return goal

# follow path from current position to goal
def follow_path(pos, path, grid):
	for cell in path:
		pos = move_to(pos, cell)
		if mode == robot.MANUAL:
			robot.stop()
			return pos
	return pos

# find next unvisited grid cell
def reachable(pos, grid):
	stderr.write("check reachability\n")
	todo = deque()
	vis = set()
	previous = dict()
	goal = None

	# do a bfs to find closest unvisited grid cell
	cur = tuple(pos[0:2])
	todo.append(cur)
	vis.add(cur)

	while todo:
		cur = todo.popleft()
		# check if current is unvisited
		if grid[cur[0]][cur[1]] == UNKNOWN:
			goal = cur
			break

		# add neighbours to queue
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
	robot.stop()
	return pos

########################################################################

# detect obstacles, find neighbour
def get_neighbour(pos, grid):
	best = -2
	aim = -1
	for i in range(0, 4):
		dot_p = vdir[0] * cos(i*pi/2.0) + vdir[1] * sin(i*pi/2.0)
		if dot_p > best:
			best = dot_p
			aim = i

	# start with right
	right = (aim + 3) % 4
	possible = None
	# we do not need to check behind the robot
	for i in range(0, 3):
		cur = (right + i) % 4
		to_check = (int(round(pos[0] + cos(cur*pi/2.0))), int(round(pos[1] + sin(cur*pi/2.0))))
		stderr.write("TRY " + str(to_check) + '\n')
		# check to see if we want to go there
		if grid[to_check[0]][to_check[1]] == UNKNOWN:
			# check to see if we can go there
			blocked = robot.detect_obstacle(i-1)
			if blocked:
				grid[to_check[0]][to_check[1]] = OBSTACLE
				robot.update_cell(robot_id, to_check, 'obstacle')
			elif possible is None:
				possible = to_check
	return possible

# explore unvisited area by following an edge
def explore(pos, grid):
	stderr.write("search area\n")
	global rows, cols, scale, discovered
	grid[pos[0]][pos[1]] = VISITED
	next_pos = get_neighbour(pos, grid)
	while next_pos is not None:
		pos = move_to(pos, next_pos)
		grid[pos[0]][pos[1]] = VISITED
		if mode == robot.MANUAL:
			robot.stop()
			return pos
		next_pos = get_neighbour(pos, grid)
	robot.stop()
	return pos

########################################################################

# assume the input has been cleaned up
# initial position of robot_pos (pair)
# to_search (visited array)
def search(robot_pos, init_dir, to_search, sc):
	global scale, rows, cols, discovered, vdir, prev_pos, mode
	discovered = 0
	rows = len(to_search)
	cols = len(to_search[0])
	scale = sc
	vdir = init_dir
	prev_pos = robot_pos

	# do the search
	robot_pos = reachable(robot_pos, to_search)
	while robot_pos is not None:
		if mode == robot.MANUAL:
			manual_mode(robot_id, robot_pos, vdir)
			mode = robot.AUTO
			break
		else:
			robot_pos = explore(robot_pos, to_search)
			robot_pos = reachable(robot_pos, to_search)
	robot.stop()
	print("DONE")

	return discovered

########################################################################

# get input and run code
def main():
	global robot_id
	robot_id = int(input())
	info = robot.get_data(robot_id)
	stderr.write("INFO: \n" + str(info) + '\n')

	# robot position and direction, convert angle to radians
	rob = tuple(info["robot_loc"])
	angle = info["robot_dir"] * pi / 180.0
	init_dir = (cos(angle), sin(angle))

	# get grid
	grid = info["grid"]

	# dimensions
	n, m = grid["grid_size"]
	to_search = [[OUTSIDE for y in range(0, m+2)] for x in range(0, n+2)]

	# search area
	for row in range(1, n+1):
		left, right = grid["to_search"][row-1]
		for col in range(left, right+1):
			to_search[row][col] = UNKNOWN

	# get scale
	scale = info["scale"]

	if robot.get_mode(robot_id) == robot.MANUAL:
		manual_mode(robot_id, 0, 0)
	else:
		# navigate
		search(rob, init_dir, to_search, scale)

print("READY")
try:
	main()
finally:
	stop()
	cleanup()
	if robot_id is not None:
		robot.set_mode(robot_id, -1)

