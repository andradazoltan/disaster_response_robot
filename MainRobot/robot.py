import subprocess
import requests
import math
import motor

#import sensors
import time

# MODES
AUTO = 0
MANUAL = 1

#################
# server requests

# get initial configuration
def get_data(r_id):
	return requests.get("http://38.88.75.83/db/robot.php?id=" + str(r_id)).json()

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

def get_joystick(r_id):
	data = requests.get("http://38.88.75.83/db/manual.php?id=" + str(r_id)).json()
	return data['dx'], data['dy']

def get_mode(r_id):
	return requests.get("http://38.88.75.83/db/manual.php?id=" + str(r_id)).json()['manual']

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

# TODO updated
# TODO CHECK THIS (and everything after this line)

# ##### TODO from a while ago, idk what this does anymore
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

# detect obstacles with sonar
def detect_obstacle(aim):
	return False

WAIT_FOR_90 = 1.3 # s
WAIT_FOR_CELL = 1.4 # s

# signed angle from -pi to pi
def rotate(angle):
	if angle > 0:
		motor.pivot(motor.LEFT, 100)
	elif angle < 0:
		motor.pivot(motor.RIGHT, 100)
	time.sleep(WAIT_FOR_90 * abs(angle) / 90.0)
	return

##### ???
def turn(direction, angle):
	radius = 45.0 / angle
	if direction == LEFT:
		motor.turn(radius, motor.LEFT, 100)
	else:
		motor.turn(radius, motor.RIGHT, 100)
	return

def straight(scale):
	motor.straight(100)
	time.sleep(WAIT_FOR_CELL)
	return

def stop():
	motor.stop()
	return
