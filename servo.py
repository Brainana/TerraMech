from gpiozero import Servo
from time import sleep

servo = Servo(27)

while True:
	servo.max()
	sleep(0.8)
	servo.mid()
	sleep(0.8)
