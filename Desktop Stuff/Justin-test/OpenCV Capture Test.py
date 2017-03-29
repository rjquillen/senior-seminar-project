from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
#Experiment with resolution and framerate for best network latency
camera.resolution = (512,384)
camera.framerate = 60
rawCapture = PiRGBArray(camera)

#Wait 0.1 seconds for camera to be ready
time.sleep(0.1)

capture = camera.capture_continuous(rawCapture, format="bgr", use_video_port = True)

for frame in capture:
    image = frame.array

    cv2.imshow("Raspberry Pi Camera Stream",image)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
    
                                       
                                       
