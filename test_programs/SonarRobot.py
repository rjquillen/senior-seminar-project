# random movements with sonar as protection from running into things

from time import sleep
import myRobotClass as mrc
from SonarClass import Sonar
from random import random

motion_delay=0.25

bob=mrc.Robot()
sue=Sonar()

def checkSonar():
    distance_check=sue.distance()
    if distance_check<20.0:
        return False
    else:
        return True

def stop_and_go():
    print 'stop and go'
    bob.stop()
    old_speed=bob.getspeed()
    bob.setSpeed(75)
    bob.backward()
    sleep(1)
    bob.stop()
    sleep(.1)
    bob.pivright()
    sleep(.5)
    bob.stop()
    bob.setSpeed(old_speed)
    if not(checkSonar()):
        stop_and_go()
    
def runBot(num):
    if num<50:
        print "forward"
        if checkSonar():
            bob.forward()
            sleep(motion_delay)
            bob.stop()
        else:
            stop_and_go()

    elif num<65:
        print "right"
        if checkSonar():
            bob.right()
            sleep(motion_delay)
            bob.stop()
        else:
            stop_and_go()

    elif num<80:
        print "left"
        if checkSonar():
            bob.left()
            sleep(motion_delay)
            bob.stop()
        else:
            stop_and_go()

    elif num<100:
        print "backward"
        if checkSonar():
            bob.backward()
            sleep(motion_delay)
            bob.stop()
        else:
            stop_and_go()

if __name__ == '__main__':
    
    try:
        while True:
            todo=int(random()*100)
            for x in range(10):
                runBot(todo)
            
    except KeyboardInterrupt:
        print("Robot stopped by keyboard interrupt")
        bob.stop()
        sue.distance()
