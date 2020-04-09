# import Tensorflow library
from imageai.Prediction.Custom import CustomImagePrediction
import datetime
# import Raspberry Pi general pin input-output library
import RPi.GPIO as gpio
import picamera
import time
import glob
import os
# import servo
from gpiozero import Servo
from time import sleep

camera = picamera.PiCamera()

#servo = Servo(27)

for f in glob.glob("lawn*.jpg"):
	os.remove(f)

# loading Tensorflow weed model
prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("resnet.hdf5")
prediction.setJsonPath("weeds_model_class.json")
print("loading Tensorflow weed model")
modelLoadStart=datetime.datetime.now()
prediction.loadModel(num_objects=9)
modelLoadEnd=datetime.datetime.now()
print("Finished loading model in " + str(modelLoadEnd-modelLoadStart))


def motorInit():
	gpio.setmode(gpio.BCM)
	gpio.setup(17, gpio.OUT)
	gpio.setup(18, gpio.OUT)
	gpio.setup(23, gpio.OUT)
	gpio.setup(24, gpio.OUT)

def motorForward(tf):
	motorInit()
	gpio.output(17, False)
	motorAGPIO = gpio.PWM(18, 100)
	motorAGPIO.start(0)
	motorAGPIO.ChangeDutyCycle(78)
	gpio.output(23, True)
	gpio.output(24, False)
	time.sleep(tf)
	motorAGPIO.stop()
	gpio.output(23, False)
	gpio.output(24, False)
#	gpio.cleanup()

def servoSpin(tf):
	servo.max()
	time.sleep(tf)
	servo.mid()
	time.sleep(3)

servo = Servo(27)

for x in range(0,5):
	print ("Robot is  moveing forward")
	motorForward(0.625)

	# Pause the robot so the camera can take a steady picture
	time.sleep(1)
	
	weedFound = False

	imageName = 'lawn' + str(x) + '.jpg'
	print ("Taking a picture of the lawn.  Image name is " + imageName)
	camera.capture(imageName)

	startImgDetection=datetime.datetime.now()
	predictions, probabilities = prediction.predictImage(imageName, result_count=3)
	endImgDetection=datetime.datetime.now()
	imgDetectionDelta=endImgDetection-startImgDetection
	print("Image detected in " + str(imgDetectionDelta))
	for eachPrediction, eachProbability in zip(predictions, probabilities):
		print(eachPrediction , " : " , eachProbability)
		if eachPrediction == "Chinee apple":
			os.rename(imageName, 'lawn' + str(x) + "_Chinee_apple.jpg")
			weedFound = True
			servoSpin(0.8);
			break

	if weedFound == False: 		
		os.rename(imageName, 'lawn' + str(x) + "_grass.jpg")

camera.close()
 
gpio.cleanup()
