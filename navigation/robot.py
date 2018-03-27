import requests
import math

#################
# server requests

# get initial configuration
def get_data(n):
	return requests.get("http://38.88.75.83/db/robot.php?id=" + str(n)).json()

def update_robot(r_id, pos):
	# TODO
	return

def update_cell(r_id, pos, value):
	# TODO
	return

#################
# RSSI stuff

# convert dbm to watts, rssi is given in dbm, we want power
def dbm_to_watts(val):
	return 10 ** (val/10.0 - 3.0)

# returns watts
def get_rssi(addr):
	rssi = -12
	# TODO
	return dbm_to_watts(rssi)

#################
# robot sensors and stuff

LEFT = 1
RIGHT = -1
STRAIGHT = 0

# TODO
# detect obstacles with sonar
def detect_obstacle(aim):
	if aim == LEFT:
		return False
	elif aim == RIGHT:
		return False
	else: # STRAIGHT
		return False

