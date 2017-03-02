import RPi.GPIO as GPIO
import time


class Sonar:
    # echo is GPIO pin 17, trig pin 21
    def __init__(self, trig=21, echo=17):
        
        self._trig=trig
        self._echo=echo
    
    def distance(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self._trig, GPIO.OUT)
        GPIO.output(self._trig, False)
        
        GPIO.setup(self._echo, GPIO.IN)
        
        time.sleep(0.015)

        print "Distance being measured"

        GPIO.output(self._trig, True)
        time.sleep(0.0001)
        GPIO.output(self._trig, False)

        while GPIO.input(self._echo)==0:
            pass
        
        pulse_start=time.time()

        while GPIO.input(self._echo)==1:
            pass

        pulse_end=time.time()

        pulse_dur=pulse_end-pulse_start

        cm_dist=round(pulse_dur*17150, 2)

        #print "Distance = "+str(cm_dist)+ "cm"

        GPIO.cleanup()
        
        return cm_dist
        
