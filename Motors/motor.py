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
MRB = 19

GPIO.setup(MRA, GPIO.OUT)
GPIO.setup(MRB, GPIO.OUT)
rightW = GPIO.HIGH

GPIO.setup(ER, GPIO.OUT)
pR = GPIO.PWM(ER, 255)
pR.start(0)

#setup left wheel
EL =  21
MLA = 22
MLB = 23

GPIO.setup(MLA, GPIO.OUT)
GPIO.setup(MLB, GPIO.OUT)
leftW = GPIO.HIGH

GPIO.setup(EL, GPIO.OUT)
pL = GPIO.PWM(EL, 255)
pL.start(0)

#set direction of robot
def setDirection(direction):
	if direction == FORWARD:
		leftW = GPIO.HIGH
		rightW = GPIO.HIGH
	else:
		leftW = GPIO.LOW
		rightW = GPIO.LOW

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
	GPIO.output(ER, GPIO.HIGH)
	GPIO.output(EL, GPIO.HIGH)

#stops the robot in its place
def stop():
	GPIO.output(ER, GPIO.LOW)
	GPIO.output(EL, GPIO.LOW)

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
	GPIO.output(ER, GPIO.HIGH)
	GPIO.output(EL, GPIO.HIGH)

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
	GPIO.output(ER, GPIO.HIGH)
	GPIO.output(EL, GPIO.HIGH)
	