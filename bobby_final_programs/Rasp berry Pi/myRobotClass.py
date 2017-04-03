# my Robot class

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit


class Robot(object):
    def __init__(self, addr=0x60, left_id=1, right_id=2, speed=100, stop_at_exit=True):

        self._mh = Adafruit_MotorHAT(addr)
        self._speed = speed

        # percentage of speed each wheel to turn at
        self._leftTrim = 1.0
        self._rightTrim = 1.0

        # wheel indi speed
        self._leftspeed = self._speed * self._leftTrim
        self._rightspeed = self._speed * self._rightTrim

        self._left = self._mh.getMotor(left_id)
        self._right = self._mh.getMotor(right_id)

        self._left.setSpeed(int(self._leftspeed))
        self._right.setSpeed(int(self._rightspeed))

        self._left.run(Adafruit_MotorHAT.RELEASE)
        self._right.run(Adafruit_MotorHAT.RELEASE)

        if stop_at_exit:
            atexit.register(self.stop)

    def forward(self):
        self._left.run(Adafruit_MotorHAT.FORWARD)
        self._right.run(Adafruit_MotorHAT.FORWARD)

    def stop(self):
        self._left.run(Adafruit_MotorHAT.RELEASE)
        self._right.run(Adafruit_MotorHAT.RELEASE)

    def backward(self):
        self._left.run(Adafruit_MotorHAT.BACKWARD)
        self._right.run(Adafruit_MotorHAT.BACKWARD)

    def right(self):
        self._left.run(Adafruit_MotorHAT.FORWARD)
        self._right.run(Adafruit_MotorHAT.RELEASE)

    def left(self):
        self._left.run(Adafruit_MotorHAT.RELEASE)
        self._right.run(Adafruit_MotorHAT.FORWARD)

    def pivright(self):
        self._left.run(Adafruit_MotorHAT.FORWARD)
        self._right.run(Adafruit_MotorHAT.BACKWARD)

    def pivleft(self):
        self._left.run(Adafruit_MotorHAT.BACKWARD)
        self._right.run(Adafruit_MotorHAT.FORWARD)

    def adjustwheels(self):
        self._leftspeed = self._speed * self._leftTrim
        self._rightspeed = self._speed * self._rightTrim
        self._left.setSpeed(int(self._leftspeed))
        self._right.setSpeed(int(self._rightspeed))

    def setSpeed(self, speed):
        self._speed = speed
        self.adjustwheels()

    def speedup(self):
        if (self._speed >= 255):
            self._speed = 255
        else:
            self._speed = self._speed + 5
        self.adjustwheels()

    def speeddown(self):
        if (self._speed <= 0):
            self._speed = 0
        else:
            self._speed = self._speed - 5
        self.adjustwheels()

    def trimright(self):
        if self._rightTrim <= self._leftTrim:
            self._rightTrim = self._rightTrim - 0.05
        else:
            self._leftTrim = self._leftTrim + 0.05
        self.adjustwheels()

    def trimleft(self):
        if self._leftTrim <= self._rightTrim:
            self._leftTrim = self._leftTrim - 0.05
        else:
            self._rightTrim = self._rightTrim + 0.05
        self.adjustwheels()

    # reset both wheels to 100%
    def resetTrim(self):
        self._leftTrim = 1.0
        self._rightTrim = 1.0
        self.adjustwheels()

    def getspeed(self):
        return self._speed

