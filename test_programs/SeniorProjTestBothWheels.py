#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
from picamera import PiCamera

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
myMotor1 = mh.getMotor(1)
myMotor2 = mh.getMotor(2)
#camera=PiCamera()

# set the speed to start, from 0 (off) to 255 (max speed)
myMotor1.setSpeed(255)
myMotor2.setSpeed(255)
#camera.start_preview()

while (True):
    
    direction=raw_input("enter direction (w,s,a,d,e,q)")
    
    if(direction == "w"):

        print "Forward"
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
        print "finished"

    if(direction == "s"):

        print "Backward"
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        time.sleep(.5)
        myMotor1.run(Adafruit_MotorHAT.RELEASE)
        myMotor2.run(Adafruit_MotorHAT.RELEASE)
        print "finished"

    if(direction == "a"):

        print "Left"
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        time.sleep(.1)
        myMotor1.run(Adafruit_MotorHAT.RELEASE)
        myMotor2.run(Adafruit_MotorHAT.RELEASE)
        print "finished"

    if(direction == "d"):

        print "Right"
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
        time.sleep(.1)
        myMotor1.run(Adafruit_MotorHAT.RELEASE)
        myMotor2.run(Adafruit_MotorHAT.RELEASE)
        print "finished"

    if(direction == "e"):

        print "stopping"
        myMotor1.run(Adafruit_MotorHAT.RELEASE)
        myMotor2.run(Adafruit_MotorHAT.RELEASE)
        print "finished"

    if(direction == "q"):
        myMotor1.run(Adafruit_MotorHAT.RELEASE)
        myMotor2.run(Adafruit_MotorHAT.RELEASE)
        print "Program done"
        break
    
#camera.stop_preview()


