import RPi.GPIO as GPIO
import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
GPIO.setmode(GPIO.BOARD)

tempCh = 3
lightCh = 2

infra = 12
GPIO.setup(infra,GPIO.OUT)

servo = 7
GPIO.setup(servo, GPIO.OUT)
servoPWM = GPIO.PWM(servo, 50)
servoPWM.start(0)

echoPin = 29
trigPin = 31
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(trigPin, GPIO.OUT)

""" Reads the brightness read on the photoresistor
    and returns the value as a percentage."""
def readLight():
    #read value from SPI and convert to transimitted value
    read = spi.xfer2([1,(8+lightCh)<<4,0])
    adc = ((read[1]&3)<<8)+read[2]
 
    return (adc/1024.0) * 100.0


""" Reads the temperature read on the LM35 sensor
    and returns it in degress Celsius."""
def readTemp():
    #read value from SPI and convert to transimitted value
    read = spi.xfer2([1,(8+tempCh)<<4,0])
    adc = ((read[1]&3)<<8)+read[2]

    #convert adc value to volts, then final temp
    volts = ((adc*0.5)/1023.0)
    temp = volts *1000.0

    return temp


""" Reads the distance read on the ultrasonic
    sensor and returns it in meters."""
def readDistance():
    startTime = 0
    endTime = 0
    
    GPIO.output(trigPin, False)
    time.sleep(1)
    GPIO.output(trigPin, True)
    time.sleep(0.00001)
    GPIO.output(trigPin, False)

    while GPIO.input(echoPin)==0:
        startTime = time.time()

    while GPIO.input(echoPin)==1:
        endTime = time.time()

    return(endTime - startTime) * 17150


""" Turns the servo motor to a specified angle
    @param angle - angle in degrees between 0 and 180
                   to turn to"""
def turnServo(angle):
    dutyCycle = angle/18 + 2
    GPIO.output(servo, True)
    servoPWM.ChangeDutyCycle(dutyCycle)
    time.sleep(1) #wait for servo to reach specified angle
    
    GPIO.output(servo, False)
    servoPWM.ChangeDutyCycle(0)


""" Turns on infrared LED
"""
def onInfrared():
    if readLight < 60:
	GPIO.output(infra, True)
    else
	GPIO.output(infra, False)
