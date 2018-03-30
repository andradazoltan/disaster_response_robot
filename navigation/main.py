import math
import sys
import navigate
import robot

# input file
# x y z rssi |
# x y z rssi |-> bluetooth
# x y z rssi |
# x y z a    --> robot, assume z = 0, a = ccw angle from +x in degrees
# n m        --> dimensions
# l r        --> left right range for row i
# scale      --> scale: unit = scale cm

def main():
	info = robot.get_data(int(input()))
	sys.stderr.write("INFO: \n" + str(info))

	# get beacons
	beacons = dict()
	for addr in info["beacon_info"]:
		beacons[addr] = [tuple(info["beacon_info"][addr])]

	# robot position and direction
	rob = tuple(info["robot_loc"])
	angle = info["robot_dir"] * math.pi / 180.0
	init_dir = (math.cos(angle), math.sin(angle))

	# get grid
	grid = info["grid"]

	# dimensions
	n, m = grid["grid_size"]
	to_search = [[navigate.OUTSIDE for y in range(0, m+2)] for x in range(0, n+2)]

	# search area
	for row in range(1, n+1):
		left, right = grid["to_search"][row-1]
		for col in range(left, right+1):
			to_search[row][col] = navigate.UNKNOWN

	# get scale
	scale = info["scale"]

	pgom = ["navigate.search(", str(beacons), str(rob), str(init_dir), str(to_search), str(scale) + " )"]
	sys.stderr.write('\n'.join(pgom) + "\n\n")

	# navigate
	res = navigate.search(beacons, rob, init_dir, to_search, scale)
	if res is not 0:
		print("ERROR: " + str(res))
	return res

print("READY")
main()

