import robot
from manual import *
from sys import stdout, stderr
from math import sqrt, pi, cos, sin, asin, acos
from collections import deque, namedtuple

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
BEACON = 7

# epsilons and errors
ANG_ROTATE = 50
ANG_ERROR = 10
DIST_ERROR = 0.368
EPS = 1e-3

# positions of the three beacons in order (pos, init rssi)
beacons = None

# grid info
discovered, rows, cols = None, None, None
scale = 1.0

# mode info
mode = robot.AUTO

# robot info
prev_pos, vdir = None, None
robot_id = None

########################################################################

# functions to calculate things
def sqr(x):
	return x*x

def dist(a, b):
	norm = 0
	for i in range(0, min(len(a), len(b))):
		norm += sqr(a[i]-b[i])
	return sqrt(norm)

def cross(a, b):
	return a[0]*b[1] - a[1]*b[0]

def get_ratio(power, distance):
	return power * sqr(distance)

def in_grid(pos):
	return pos[0] >= 0 and pos[1] >= 0 and pos[0] < rows and pos[1] < cols

def direction(s, t):
	x, y = t[0]-s[0], t[1]-s[1]
	norm = sqrt(sqr(x) + sqr(y))
	return (float(x)/norm, float(y)/norm)

# return intersection of c1 and c2 that is closest to c3
def cc_inter(c1, c2, c3):
	vec = (c2.x - c1.x, c2.y - c1.y)
	dist_sqr = float(sqr(vec[0]) + sqr(vec[1]))
	diff_sqr = float(sqr(c1.r) - sqr(c2.r))
	radi_sqr = float(sqr(c1.r) + sqr(c2.r))
	perp = (0.5 * (c1.x + c2.x + vec[0] * diff_sqr / dist_sqr),
			0.5 * (c1.y + c2.y + vec[1] * diff_sqr / dist_sqr))
	difference = 2.0 * dist_sqr * radi_sqr - sqr(dist_sqr) - sqr(diff_sqr)
	if difference < EPS:
		return perp
	else:
		factor = 0.5 * sqrt(difference) / dist_sqr
		i1 = (perp[0] + factor * (-vec[1]), perp[1] + factor * (vec[0]))
		i2 = (perp[0] - factor * (-vec[1]), perp[1] - factor * (vec[0]))
		if abs(dist(i1, (c3.x, c3.y)) - c3.r) < abs(dist(i2, (c3.x, c3.y)) - c3.r):
			return i1
		else:
			return i2

########################################################################

def grid_index():
	circle = []
	for addr in beacons:
		x, y, z = beacons[addr][0]
		length_sqr = beacons[addr][1] / robot.get_rssi(addr)
		radius = sqrt(length_sqr - sqr(z))
		circle.append(Circle(x, y, radius))

	# cc inter
	inter = (0,0)
	for i in range(0, 3):
		point = cc_inter(circle[i], circle[(i+1)%3], circle[(i+2)%3])
		inter = (inter[0] + point[0] / 3.0, inter[1] + point[1] / 3.0)

	print(inter)
	global vdir, prev_pos
	# update prev_pos and vdir
	if dist(inter, prev_pos) > DIST_ERROR:
		vdir = direction(prev_pos, inter)
		prev_pos = inter

	return (int(round(inter[0])), int(round(inter[1])))

# TODO i think we just change this thing
# TODO probably very wrong
# move robot from cur to goal
def move_to(cur, goal):
	global vdir, mode
	robot.update_cell(robot_id, cur, 'visited')

	# left, straight, right ?
	aim = direction(cur, goal)

	# get angle
	angle = asin(cross(vdir, aim))
	# check if this angle is obtuse
	if dot_p(vdir, aim) < 0:
		angle = pi - angle

	# rotate to correct direction
	robot.rotate(angle)

	# move to next cell
	robot.straight(scale)

	# update vdir
	vdir = direction(cur, goal)

	# get auto / manual
	mode = robot.get_mode(robot_id)

	# update robot
	robot.update_robot(robot_id, cur, vdir)
	robot.update_cell(robot_id, cur, 'robot')

	return goal

# follow path from current position to goal
def follow_path(pos, path, grid):
	# stderr.write("PATH: " + str(path) + '\n\n')
	for cell in path:
		pos = move_to(pos, cell)
		if mode == robot.MANUAL:
			robot.stop()
			return pos
	# stderr.write("done path ~~~ \n\n")
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
	robot.stop()
	return pos

########################################################################

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
	# stderr.write(" @ " + str(pos) + '\n')
	# we do not need to check behind the robot
	for i in range(0, 3):
		cur = (left + i) % 4
		to_check = (int(round(pos[0] + cos(cur*pi/2))), int(round(pos[1] + sin(cur*pi/2))))
		# stderr.write("TRY " + str(to_check) + '\n')
		# check to see if we want to go there
		if grid[to_check[0]][to_check[1]] == UNKNOWN:
			# check to see if we can go there
			blocked = robot.detect_obstacle(i-1)
			if blocked:
				grid[to_check[0]][to_check[1]] = OBSTACLE
				robot.update_cell(robot_id, to_check, 'obstacle')
			elif possible is None:
				possible = to_check
	# stderr.write("neighbour from " + str(pos) + " : " + str(possible) + '\n')
	return possible

# explore unvisited area by following the right edge
def explore(pos, grid):
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
# positions of the three beacons in order (pos, init rssi)
# initial position of robot_pos (pair)
# to_search (visited array)
def search(init_beacons, robot_pos, init_dir, to_search, sc):
	global scale, rows, cols, discovered, vdir, prev_pos, beacons
	discovered = 0
	rows = len(to_search)
	cols = len(to_search[0])
	scale = sc
	beacons = init_beacons
	vdir = init_dir
	prev_pos = robot_pos

	# initialize beacon dist
	for addr in beacons:
		to_search[beacons[addr][0][0]][beacons[addr][0][1]] = BEACON
		beacons[addr].append(get_ratio(robot.get_rssi(addr), dist(robot_pos, beacons[addr][0])))

	''' # debug
	stderr.write("scale: " + str(scale) + '\n')
	stderr.write("init beacons: \n" + '\n'.join(map(str, beacons)) + '\n')
	stderr.write("init robot: " + str(robot_pos) + '\n')
	stderr.write("init dir: " + str(vdir) + '\n')
	stderr.write("to_search: \n" + '\n'.join(map(str, to_search)) + '\n')
	stderr.write("END INITIAL DEBUG\n\n")
	'''

	# do the search
	robot_pos = reachable(robot_pos, to_search)
	while robot_pos is not None:
		if mode == robot.MANUAL:
			robot_pos = manual_mode(robot_id, robot_pos, vdir)
		else:
			robot_pos = explore(robot_pos, to_search)
		if mode != robot.MANUAL:
			robot_pos = reachable(robot_pos, to_search)
	robot.stop()
	print("DONE")

	return discovered

########################################################################

# input file
# x y z rssi |
# x y z rssi |-> bluetooth
# x y z rssi |
# x y z a    --> robot, assume z = 0, a = ccw angle from +x in degrees
# n m        --> dimensions
# l r        --> left right range for row i
# scale      --> scale: unit = scale cm

def main():
	global robot_id
	robot_id = int(input())
	info = robot.get_data(robot_id)
	sys.stderr.write("INFO: \n" + str(info))

	# get beacons
	beacons = dict()
	for addr in info["beacon_info"]:
		beacons[addr] = [tuple(info["beacon_info"][addr])]

	# robot position and direction
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

	# navigate
	res = search(beacons, rob, init_dir, to_search, scale)
	if res is not 0:
		print("ERROR: " + str(res))
	return res

print("READY")
main()

