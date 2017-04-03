# robot controled by wii with sonar sensor
# ability to turn in and out of random mode

# imports
import cwiid            # Wii Remote library
from time import sleep
from time import time
import myRobotClass as mrc
from SonarClass import Sonar
from random import random
import threading

motion_delay = 0.25
button_delay = 0.1

bob = mrc.Robot()
sue = Sonar()

go2 = True
go3 = True

# connect wii remote
print "press 1 + 2 on your wii remote"
sleep(1)
while 1:
    try:
        wii = cwiid.Wiimote()
        break
    except:
        print "Error opening wii remote\nTrying again"


# check sonar if close
def checkSonar():
    global go2
    global go3
    while go3:
        while go2 and go3:
            if sue.distance() < 20.0:
                go2 = False
            sleep(.1)


# get out if check sonar returns False
def stop_and_go():
    print 'stop and go'
    bob.stop()
    old_speed = bob.getspeed()
    bob.setSpeed(75)
    bob.backward()
    sleep(1)
    bob.stop()
    sleep(.1)
    bob.pivright()
    sleep(.5)
    bob.stop()
    bob.setSpeed(old_speed)


# go from wii control directions
def go(direction):
    # forward
    if direction == "w":
        bob.forward()
        sleep(button_delay)
        bob.stop()

    # backwards
    elif direction == "s":
        bob.backward()
        sleep(button_delay)
        bob.stop()

    # left
    elif direction == "a":
        bob.left()
        sleep(button_delay)
        bob.stop()

    # right
    elif direction == "d":
        bob.right()
        sleep(button_delay)
        bob.stop()

    # piv right
    elif direction == "e":
        bob.pivright()
        sleep(button_delay)
        bob.stop()

    # piv left
    elif direction == "q":
        bob.pivleft()
        sleep(button_delay)
        bob.stop()

    # speed up
    elif direction == "u":
        bob.speedup()
        sleep(button_delay)
        print bob.getspeed()

    # speed down
    elif direction == "j":
        bob.speeddown()
        sleep(button_delay)
        print bob.getspeed()

    # trim right
    elif direction == "k":
        bob.trimright()
        sleep(button_delay)
        print bob.getspeed()

    # trim left
    elif direction == "h":
        bob.trimleft()
        sleep(button_delay)
        print bob.getspeed()

    # reset trim
    elif direction == "r":
        bob.resetTrim()
        sleep(button_delay)
        print bob.getspeed()


# go from randomBot directions
def runBot(num):
    if num < 50:
        print "forward"
        bob.forward()
        sleep(motion_delay)
        bob.stop()

    elif num < 65:
        print "right"
        bob.pivright()
        sleep(motion_delay)
        bob.stop()

    elif num < 80:
        print "left"
        bob.pivleft()
        sleep(motion_delay)
        bob.stop()

    elif num < 100:
        print "backward"
        bob.backward()
        sleep(motion_delay)
        bob.stop()


# random directions until 'A' is pressed on wii
def randomBot():
    global go2

    print "\nRandom Bot!!! :D\n"

    while True:
        while True:

            # reset states
            buttons = wii.state['buttons']

            if (buttons & cwiid.BTN_A):
                print "\nEnding Random Bot :`(\n"
                wii.led = 1
                return

            todo = int(random() * 100)
            for x in range(5):
                wii.led = int(random() * 100) % 15 + 1
                if go2:
                    runBot(todo)
                else:
                    stop_and_go()
                    go2 = True


# set wii remote
wii.rpt_mode = cwiid.RPT_BTN

thread1 = threading.Thread(target=checkSonar)
thread1.start()

# loop to get buttons
while True:

    while go2:

        # reset states
        buttons = wii.state['buttons']

        # end program
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
            print "closing connection..."
            wii.rumble = 1
            sleep(1)
            wii.rumble = 0
            wii.led = 0
            go3 = False
            sleep(1)
            exit(wii)

        # backward
        elif (buttons & cwiid.BTN_LEFT):
            go("s")

        # forward
        elif (buttons & cwiid.BTN_RIGHT):
            go("w")

        # left
        elif (buttons & cwiid.BTN_UP):
            go("a")

        # right
        elif (buttons & cwiid.BTN_DOWN):
            go('d')

        # piv left
        elif (buttons & cwiid.BTN_1):
            if (buttons & cwiid.BTN_2):
                wii.rumble = 1
                sleep(0.5)
                wii.rumble = 0
                randomBot()
                wii.rumble = 1
                sleep(0.5)
                wii.rumble = 0
            else:
                go('q')

        # piv right
        elif (buttons & cwiid.BTN_2):
            go('e')

        # increase speed
        elif (buttons & cwiid.BTN_A):
            go("u")

        # decrease speed
        elif (buttons & cwiid.BTN_B):
            go('j')

        # reset trim
        elif (buttons & cwiid.BTN_HOME):
            go('r')

        # trim right
        elif (buttons & cwiid.BTN_MINUS):
            go('k')

        # trim left
        elif (buttons & cwiid.BTN_PLUS):
            go('h')

    stop_and_go()
    go2 = True
