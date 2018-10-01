import motor

import subprocess
import requests
import math
import time
from sensors import readDistance, turnServo
from sys import stderr

# ROBOT MODES
AUTO = 0
MANUAL = 1

##################### SERVER REQUEST FUNCTIONS #########################

# get initial configuration
def get_data(r_id):
	return requests.get("http://38.88.75.83/db/robot.php?id=" + str(r_id)).json()

# update robot in database
def update_robot(r_id, pos, vdir):
	requests.post(
			"http://38.88.75.83/db/updatelocation.php?id="+str(r_id),
			data = {
				'robotX':pos[0], 
				'robotY':pos[1], 
				'robotdir':math.atan2(vdir[1],vdir[0]) * 180/math.pi,
				'temp':24
			}
	)
	return

# update grid cell in database
def update_cell(r_id, pos, status):
	requests.post(
			"http://38.88.75.83/db/updategrid.php?id="+str(r_id),
			data = {
				'xpos':pos[0],
				'ypos':pos[1],
				'status':status
			}
	)
	return

# get joystick values
def get_joystick(r_id):
	data = requests.get("http://38.88.75.83/db/manual.php?id=" + str(r_id)).json()
	return data['dx'], data['dy']

# get mode (manual, auto, inactive)
def get_mode(r_id):
	return requests.get("http://38.88.75.83/db/manual.php?id=" + str(r_id)).json()['manual']

# set mode (manual, auto, inactive) 
def set_mode(r_id, mode):
	requests.post(
		"http://38.88.75.83/db/setmode.php?id="+str(r_id), 
		data = { 'manual':mode }
	)
	return

########################### ROBOT COMMANDS ############################

LEFT = 1
RIGHT = -1
STRAIGHT = 0
obstacle_dist = 15 # distance to obstacle in cm

# wait times
WAIT_FOR_90 = 1.0 # s
WAIT_FOR_CELL = 1.0 # s

# search for obstacles using the ultrasound sensor
def detect_obstacle(aim):
	stderr.write("look " + str(aim) + '\n')
	dist = 100
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

# command the robot to turn an angle of -pi to pi
def rotate(angle):
	stderr.write("rotate by " + str(angle) + '\n')
	if angle > 0:
		motor.pivot(motor.LEFT, 100)
	elif angle < 0:
		motor.pivot(motor.RIGHT, 100)
	time.sleep(WAIT_FOR_90 * abs(angle) / 90.0)
	motor.stop()
	return

# direct robot to go straight
def straight():
	stderr.write("forwards\n")
	motor.straight(100)
	time.sleep(WAIT_FOR_CELL)
	motor.stop()
	return

# stop the robot
def stop():
	motor.stop()
	return
