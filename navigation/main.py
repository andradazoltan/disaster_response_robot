import math
import sys
import navigate

# input file
# x y z rssi |
# x y z rssi |-> bluetooth
# x y z rssi |
# x y z a    --> robot, assume z = 0, a = ccw angle from +x in degrees
# n m        --> dimensions
# l r        --> left right range for row i
# scale      --> scale: unit = scale cm

def dbm_to_watts(val):
	return 10 ** (val/10.0 - 3.0)

# beacon positions
beacons = []
for i in range(0, 3):
	line = [int(x) for x in input().strip().split()]
	beacons.append([tuple(line[0:3]), dbm_to_watts(line[-1])])

# robot position
line = [int(x) for x in input().strip().split()]
angle = line[3] * math.pi / 180.0
init_dir = (math.cos(angle), math.sin(angle))
robot = tuple(line[0:3])

# dimensions
n, m = map(int, input().strip().split())
to_search = [[navigate.OUTSIDE for y in range(0, m+2)] for x in range(0, n+2)]

print (n)
# lines
for row in range(1, n+1):
	left, right = map(int, input().strip().split())
	for col in range(left, right+1):
		to_search[row][col] = navigate.UNKNOWN

# get scale
scale = float(input())

# navigate
res = navigate.search(beacons, robot, init_dir, to_search, scale)
if res is not 0:
	print("ERROR: " + str(res))

