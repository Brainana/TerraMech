import RPi.GPIO as gpio
import time

gpio.setwarnings(False)

def init():
	gpio.setmode(gpio.BCM)
	gpio.setup(17, gpio.OUT)
	gpio.setup(18, gpio.OUT)
	gpio.setup(23, gpio.OUT)
	gpio.setup(24, gpio.OUT)

def forward(tf):
	init()
	
	gpio.output(17, False)
	motorAGPIO = gpio.PWM(18, 100)
	motorAGPIO.start(0)
	motorAGPIO.ChangeDutyCycle(100)
#	p1.start(0)
#	p2.start(0)
#	p1.ChangeDutyCycle(100)
	gpio.output(23, True)
	gpio.output(24, False)

	time.sleep(tf)
	motorAGPIO.stop()
#	p1.stop()
#	p2.stop()
	gpio.cleanup()
print ("forward")
forward(2) 
