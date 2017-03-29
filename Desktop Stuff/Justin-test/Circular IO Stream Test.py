
from picamera import PiCamera
from picamera.streams import PiCameraCircularIO
import time
import socket

host="136.227.162.110"
port=5060

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

camera = PiCamera()

camera.resolution = (640,480)
camera.framerate = 32

stream = PiCameraCircularIO(camera,seconds=10)
stream.copy_to(
