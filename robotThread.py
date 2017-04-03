from time import sleep
import RPi.GPIO as GPIO
import threading
from sensorThread import *
import myRobotClass as mrc
import Queue

class RobotThread(threading.Thread):

    def __init__(self, mainResume, sensorStop, goEvent, commandSet, commandQueue, sensorRetQueue):
        super(RobotThread, self).__init__()
        # threading events
        self.mainResume = mainResume
        self.sensorStop = sensorStop
        self.goEvent = goEvent
        #self.stateReady = stateReady
        self.commandSet = commandSet
        self.stopRequest = threading.Event()
        # Queues to get and return values from thread
        self.commandQueue = commandQueue
        self.sensorRetQueue = sensorRetQueue
        self.bob = mrc.Robot()

    def stopAndGo(self):
        #print "Stop and going"
        self.bob.stop()
        oldSpeed = self.bob.getspeed()
        self.bob.setSpeed(75)
        self.bob.backward()
        sleep(1)
        self.bob.stop()
        sleep(.1)
        self.bob.pivright()
        sleep(.5)
        self.bob.stop()
        self.bob.setSpeed(oldSpeed)

    def dataRead():
        while not commandQueue.empty():
            data = commandQueue.get()
            print str(data)
            if str(data).lower()=='exit':
                #self.s.close()
                #print "end of server"
                sleep(1)
                print "end of program"
                break
            if str(data).lower()=='forward':
                self.bob.forward()
                sleep(button_delay)
                self.bob.stop()
            elif str(data).lower()=='left':
                self.bob.left()
                sleep(button_delay)
                self.bob.stop()
            elif str(data).lower()=='right':
                self.bob.right()
                sleep(button_delay)
                self.bob.stop()
            elif str(data).lower()=='right_trim':
                self.bob.trimright()
            elif str(data).lower()=='left_trim':
                self.bob.trimleft()
            else:
                print "not a recognized command"
                continue
        self.commandSet.clear()


    def run(self):
        #button_delay = 0.1
        # sensor read queue, last in first out (always get most recent sensor read)
        #sensorReads = Queue.LifoQueue()
        #initialize robot speed
        self.bob.setSpeed(100)
        # initialize obstacle distance to 0
        #obDistance =  0
        
        # create sensor thread object, start thread
        #sensor = SensorThread(0, self.stopEvent, self.goEvent, self.mainResume, sensorReads)
        #sensor.start()

        # run loop continues as long as join() has not been called from piMain
        while not self.stopRequest.isSet():
            self.goEvent.wait()
            while self.sensorStop.isSet():
                # clear mainResume event such that main waits CURRENTLY TESTING IN SENSORTHREAD
                # self.mainResume.clear()
                
                #print "Stopping!"
                # put problematic distance in return queue to main thread
                #retDist = self.sensorRetQueue.get()
                #self..put(retDist)
                # perform stop and go
                self.stopAndGo()
                # notify main to resume
                self.mainResume.set()
                # wait on go event signal from main thread (MOVED UP FOR NOW)
                #self.goEvent.wait()
                #continue
                break

            if self.commandSet.isSet():
                comm = self.commandQueue.get()
                print "Comm = " + str(comm)
                continue
            
            #while not self.stopEvent.isSet() and self.goEvent.isSet():
                #if commandReady.isSet:
                    #command = workQueue.get()
                    #dataRead(command)
                    #commandReady.clear()
            #else:
                
            # get directions if frame has been analyzed
        print "Joining sensor"
        sensor.join()

    def join(self, timeout = None):
        self.stopRequest.set()
        super(RobotThread, self).join(timeout)
