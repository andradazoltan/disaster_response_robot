from robot import get_joystick, get_mode
from motor import *

def manual_mode(r_id):
	while True:
		x, y = get_joystick(r_id)
		
		pwmValue = abs(y)/1.0 * 100.0
		radius = 1.0 - (abs(x)/1.0)

		if y < 0:
			setDirection(BACKWARD)
		else
			setDirection(FORWARD)

		if radius == 0:
			straight(pwmValue)
		else:	
			if x < 0:
				turn(radius, LEFT, pwmValue)
			else:
				turn(radius, RIGHT, pwmValue)

		mode = get_mode(r_id)
		if mode != 1:
			return mode
