import picamera
import time

camera = picamera.PiCamera()
for x in range(0, 5):
   name = 'example0' + str(x) + '.jpg'
   print (name)  
   camera.capture(name)
   time.sleep(3)

camera.close()
