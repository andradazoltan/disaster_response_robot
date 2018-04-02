import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

#setup direction and speed constants
LEFT = 1
RIGHT = 0
FORWARD = 1
BACKWARD = 0

#SETUP MOTORS
#setup right wheel
ER = 16
MRA = 18
MRB = 22

GPIO.setup(MRA, GPIO.OUT)
GPIO.setup(MRB, GPIO.OUT)
rightW = True

GPIO.setup(ER, GPIO.OUT)
pR = GPIO.PWM(ER, 100)
pR.start(0)

#setup left wheel
EL =  11
MLA = 13
MLB = 15

GPIO.setup(MLA, GPIO.OUT)
GPIO.setup(MLB, GPIO.OUT)
leftW = True

GPIO.setup(EL, GPIO.OUT)
pL = GPIO.PWM(EL, 100)
pL.start(0)

#set direction of robot
def setDirection(direction):
	if direction == FORWARD:
		leftW = True
		rightW = True
	else:
		leftW = False
		rightW = False

#set PWM to control speed of wheels
def setPWM(pwmValue):
	pR.ChangeDutyCycle(pwmValue)
	pL.ChangeDutyCycle(pwmValue)

#robot moves straight at a given PWM value
def straight(pwmValue):
	GPIO.output(MRA, rightW)
	GPIO.output(MRB, not rightW)
	GPIO.output(MLA, leftW)
	GPIO.output(MLB, not leftW)
	
	setPWM(pwmValue)
	GPIO.output(ER, True)
	GPIO.output(EL, True)

#stops the robot in its place
def stop():
	setPWM(0)

#robot rotates on the spot
def pivot(direction, pwmValue):
	if direction == LEFT:
		GPIO.output(MRA, rightW)
		GPIO.output(MRB, not rightW)
		GPIO.output(MLA, not leftW)
		GPIO.output(MLB, leftW)
	else:
		GPIO.output(MRA, not rightW)
		GPIO.output(MRB, rightW)
		GPIO.output(MLA, leftW)
		GPIO.output(MLB, not leftW)
	
	setPWM(pwmValue)
	GPIO.output(ER, True)
	GPIO.output(EL, True)

#robot turns in a circular arc of specified radius
def turn(radius, direction, pwmValue):
	factor = radius/(radius+14)
	GPIO.output(MRA, rightW)
	GPIO.output(MRB, not rightW)
	GPIO.output(MLA, leftW)
	GPIO.output(MLB, not leftW)

	if direction == LEFT:
		pR.ChangeDutyCycle(pwmValue*factor)
		pL.ChangeDutyCycle(pwmValue)
	else:
		pR.ChangeDutyCycle(pwmValue)
		pL.ChangeDutyCycle(pwmValue*factor)
	GPIO.output(ER, True)
	GPIO.output(EL, True)
	