import time
import RPi.GPIO as GPIO
import threading

TRIG = 21
ECHO = 17

class SensorThread(threading.Thread):

    # class constructor
    def __init__(self, sensorStop, goEvent, mainResume, retQueue):
        super(SensorThread, self).__init__()
        self.retQueue = retQueue
        self.goEvent = goEvent
        self.sensorStop = sensorStop
        self.mainResume = mainResume
        self.stopRequest = threading.Event()
        self.gpioTrig = TRIG
        self.gpioEcho = ECHO

    # definition of distance function 
    def distance(self):

        # initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioTrig, GPIO.OUT)
        GPIO.output(self.gpioTrig, False)
        GPIO.setup(self.gpioEcho, GPIO.IN)

        # measure distance
        #print "Distance being measured"
        GPIO.output(self.gpioTrig, True)
        time.sleep(0.0001)
        GPIO.output(self.gpioTrig, False)

        # ensure echo not set
        while GPIO.input(self.gpioEcho)==0:
            pass

        # set start time
        pulse_start=time.time()

        # ensure echo is set
        while GPIO.input(self.gpioEcho)==1:
            pass

        # calculate duration of ping, then distance of closest object detected
        pulse_end=time.time()
        pulse_dur=pulse_end-pulse_start
        
        cm_dist=round(pulse_dur*17150, 2)
        #print "Distance = "+str(cm_dist)+ "cm"

        # clean up GPIO settings
        GPIO.cleanup()
        # return distance
        return cm_dist
    
    #definiion of run
    def run(self):
        # continue run loop as long as join() has not been called
        while not self.stopRequest.isSet():
            self.goEvent.wait()
            while self.goEvent.isSet() and not self.sensorStop.isSet():
                #print "getting distance!"
                time.sleep(0.015)
                obDistance = self.distance()
                if obDistance <= 20:
                    print "Obstacle detected"
                    self.retQueue.put(obDistance)
                    # clear mainResume from this level when obstacle detected
                    self.sensorStop.set()
                    self.mainResume.clear()
                    break
                    #self.goEvent.wait()
            #print "either go not set or stop is set"

    # definition of join, sets stop request
    def join(self, timeout = None):
        # set own stop request and join thread
        self.stopRequest.set()
        super(SensorThread, self).join(timeout)
