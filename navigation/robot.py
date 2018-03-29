import subprocess
import requests
import math

import sensors
import time

#################
# server requests

# get initial configuration
def get_data(n):
	return requests.get("http://38.88.75.83/db/robot.php?id=" + str(n)).json()

def update_robot(r_id, pos, vdir):
	requests.post(
			"http://38.88.75.83/db/updatelocation.php?id="+str(r_id),
			data = {
				'robotX':pos[0], 
				'robotY':pos[1], 
				'robotdir':math.atan2(vdir[1],vdir[0]) * 180/math.pi
			}
	)
	return

def update_cell(r_id, pos, value):
	# get status
	status = 'unknown'
	if value == 1:
		status = 'empty'
	elif value == 2:
		status = 'obstacle'
	elif value == 3:
		status = 'object'

	requests.post(
			"http://38.88.75.83/db/updategrid.php?id="+str(r_id),
			data = {
				'xpos':pos[0],
				'ypos':pos[1],
				'status':status
			}
	)
	return

#################
# RSSI stuff

# convert dbm to watts, rssi is given in dbm, we want power
def dbm_to_watts(val):
	return 10 ** (val/10.0 - 3.0)

# returns watts
def get_rssi(addr):
	rssi = subprocess.check_output(['hcitool', 'rssi', addr]).strip().split()[-1]
	return dbm_to_watts(float(rssi))

#################
# robot sensors and stuff

LEFT = 1
RIGHT = -1
STRAIGHT = 0
obstacle_dist = 15 # distance to obstacle in cm

# TODO CHECK THIS (and everything after this line)
# detect obstacles with sonar
def detect_obstacle(aim):
	if aim == LEFT:
		turnServo(180)
		dist = readDistance()
		turnServo(90)
	elif aim == RIGHT:
		turnServo(0)
		dist = readDistance()
		turnServo(90)
	else: # STRAIGHT
		dist = readDistance()

	if dist > obstacle_dist:
		return False
	else:
		return True

WAIT_FOR_90 = 1.3 # s

def rotate(direction, angle):
	if direction == LEFT:
		motor.pivot(motor.LEFT, 100)
	else:
		motor.pivot(motor.RIGHT, 100)
	time.sleep(WAIT_FOR_90 * angle / 90.0)
	return

def turn(direction, angle):
	radius = 45.0 / angle
	if direction == LEFT:
		motor.turn(radius, motor.LEFT, 100)
	else:
		motor.turn(radius, motor.RIGHT, 100)
	return

def straight():
	straight(100)
	return

def stop():
	motor.stop()
	return
