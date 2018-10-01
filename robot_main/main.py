import robot
from automatic import automatic_mode
from manual import manual_mode
from motor import cleanup, stop

from sys import stderr
from math import pi, cos, sin

############################## MAIN CODE ###############################

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
	to_search = [[automatic.OUTSIDE for y in range(0, m+2)] for x in range(0, n+2)]

	# search area
	for row in range(1, n+1):
		left, right = grid["to_search"][row-1]
		for col in range(left, right+1):
			to_search[row][col] = automatic.UNKNOWN

	# get scale
	scale = info["scale"]

	if robot.get_mode(robot_id) == robot.MANUAL:
		manual_mode(robot_id, 0, 0)
	else:
		# navigate
		automatic_mode(rob, init_dir, to_search, scale)

try:
	main()
finally:
	stop()
	cleanup()
	if robot_id is not None:
		robot.set_mode(robot_id, -1)

