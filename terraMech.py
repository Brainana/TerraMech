# import Tensorflow library
from imageai.Prediction.Custom import CustomImagePrediction
import datetime
# import Raspberry Pi general pin input-output library
import RPi.GPIO as gpio
import picamera
import time
import glob
import os
import subprocess
# import servo
from gpiozero import Servo
from time import sleep

cameraEnable = True;
motorEnable = True;
tensorflowEnable = True;
servoEnable = True;
speakerEnable = True;

camera = picamera.PiCamera()

#servo = Servo(27)

subprocess.run(["aplay", "start.wav"])
time.sleep(0.5)

for f in glob.glob("lawn*.jpg"):
	os.remove(f)

if tensorflowEnable:
	# loading Tensorflow weed model
	prediction = CustomImagePrediction()
	prediction.setModelTypeAsResNet()
	prediction.setModelPath("resnet.hdf5")
	prediction.setJsonPath("weeds_model_class.json")
	print("loading Tensorflow weed model")
	subprocess.run(["aplay", "model.wav"])
	modelLoadStart=datetime.datetime.now()
	prediction.loadModel(num_objects=9)
	modelLoadEnd=datetime.datetime.now()
	print("Finished loading model in " + str(modelLoadEnd-modelLoadStart))
	subprocess.run(["aplay", "modelDone.wav"])
	time.sleep(0.5)


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
	if motorEnable:
		print ("Robot is  moving forward")
		subprocess.run(["aplay", "move.wav"])
		motorForward(0.625)

	# Pause the robot so the camera can take a steady picture
	time.sleep(1)
	
	weedFound = False

	if cameraEnable:
		imageName = 'lawn' + str(x) + '.jpg'
		print ("Taking a picture of the lawn.  Image name is " + imageName)
		subprocess.run(["aplay", "picture.wav"])
		time.sleep(0.5)
		camera.capture(imageName)
		if tensorflowEnable:
			subprocess.run(["aplay", "analyze.wav"])
			startImgDetection=datetime.datetime.now()
			predictions, probabilities = prediction.predictImage(imageName, result_count=3)
			endImgDetection=datetime.datetime.now()
			imgDetectionDelta=endImgDetection-startImgDetection
			time.sleep(0.5)
			print("Image detected in " + str(imgDetectionDelta))
			for eachPrediction, eachProbability in zip(predictions, probabilities):
				print(eachPrediction , " : " , eachProbability)
				if eachPrediction == "Chinee apple":
					os.rename(imageName, 'lawn' + str(x) + "_Chinee_apple.jpg")
					weedFound = True
					subprocess.run(["aplay", "weed.wav"])		
					time.sleep(1)
					if servoEnable:
						servoSpin(0.8);
					break

			if weedFound == False: 		
				os.rename(imageName, 'lawn' + str(x) + "_grass.jpg")
				subprocess.run(["aplay", "grass.wav"])
				time.sleep(0.5)

camera.close()
 
gpio.cleanup()

subprocess.run(["aplay", "end.wav"])
