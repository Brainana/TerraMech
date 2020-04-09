# import Tensorflow library
#from imageai.Prediction.Custom import CustomImagePrediction
import datetime
# import Raspberry Pi general pin input-output library
import RPi.GPIO as gpio
import picamera
import time
import os

camera = picamera.PiCamera()

# loading Tensorflow weed model
#prediction = CustomImagePrediction()
#prediction.setModelTypeAsResNet()
#prediction.setModelPath("resnet.hdf5")
#prediction.setJsonPath("weeds_model_class.json")
#print("loading Tensorflow weed model")
#modelLoadStart=datetime.datetime.now()
#prediction.loadModel(num_objects=9)
#modelLoadEnd=datetime.datetime.now()
#print("Finished loading model in " + str(modelLoadEnd-modelLoadStart))


def motorInit():
	gpio.setmode(gpio.BCM)
	gpio.setup(17, gpio.OUT)
	gpio.setup(22, gpio.OUT)
	gpio.setup(23, gpio.OUT)
	gpio.setup(24, gpio.OUT)

def motorForward(tf):
	motorInit()
	gpio.output(17, False)
	gpio.output(22, True)
	gpio.output(23, False)
	gpio.output(24, True)
	time.sleep(tf)
	gpio.cleanup()

def servoSpin(tf):
	servo.max()
	time.sleep(tf)

#servo.min()

for x in range(0,5):
	print ("Robot is  moveing forward")
	motorForward(0.625)

	# Pause the robot so the camera can take a steady picture
	time.sleep(1)
	
	imageName = 'lawn' + str(x) + '.jpg'
	print ("Taking a picture of the lawn.  Image name is " + imageName)
	camera.capture(imageName)

#	startImgDetection=datetime.datetime.now()
#	predictions, probabilities = prediction.predictImage(imageName, result_count=3)
#	endImgDetection=datetime.datetime.now()
#	imgDetectionDelta=endImgDetection-startImgDetection
#	print("Image detected in " + str(imgDetectionDelta))
#	for eachPrediction, eachProbability in zip(predictions, probabilities):
#		print(eachPrediction , " : " , eachProbability)

	os.rename(imageName, 'lawn' + str(x) + "_" + "test" + ".jpg")
#	servoSpin(1);

camera.close() 
