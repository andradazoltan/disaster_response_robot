import RPi.GPIO as GPIO
import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
GPIO.setmode(GPIO.BOARD)

tempCh = 5
lightCh = 2

hsIN = 12
hsOUT = 12

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



""" Initializes communiction with DHT11 sensor and
    reads in data from the sensor. Returns air humidity
    as a percentage."""
def readHumidity():
    GPIO.setup(hsOUT, GPIO.OUT)
    #set data line to high to indicate start signal
    GPIO.output(hsOUT, True)
    time.sleep(0.25)

    #set data line low for 20micro s
    GPIO.output(hsOUT, False)
    time.sleep(0.02)

    #end start signal by setting data line high for 40micro s
    GPIO.output(hsOUT, True)
    time.sleep(0.00004)

    #start reading data line
    GPIO.setup(hsIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    time.sleep(0.00001)
   
    #first: expect a low response from sensor for 80micro s
    while GPIO.input(hsIN) != 0:
            time.sleep(0.0000001)
    time.sleep(0.00008)
    
    #second: expect a high response from sensor for 80micro s
    while GPIO.input(hsIN) != 1:
        time.sleep(0.0000001)
    time.sleep(0.00008)
    
    #start to read incoming data, data sent as such:
        #50micro s
        #if 30micro s HIGH pulse, data = 0
        #else, data = 1
    times = [None]*80
    data = [None]*5
    for i in range(0,80):
        times[i] = (getMicroSeconds(0))
        times[i+1] = (getMicroSeconds(1))
   
    #parse through read times to see what data bits were sent
    for i in range(0,40):
        lowtime = times[2*i]
        hightime = times[2*i+1]

        data[i/8] <<= 1

        if hightime > lowtime:
            data[i/8] |= 1
    return data[0]

""" Returns the amount of microseconds the humidity
    sensor is outputting a certain signal level."""
def getMicroSeconds(level):
    count = 0
    while GPIO.input(hsIN) == level:
        count += 1
        time.sleep(0.00001)
        print(level)
        
    return count

if __name__ == '__main__':
    try:
        while True:
            light = readHumidity()
            print(light)
            time.sleep(1)
          
    except KeyboardInterrupt:
        GPIO.cleanup()
    
