
import Queue
from robotThread import *
from networkData import *
import sys

#main function definition
def main():

    # threading events for robot stop, robot go, and main to resume respectively
    sensorStop = threading.Event()
    go = threading.Event()
    resume = threading.Event()
    receiveReady = threading.Event()
    sendReady = threading.Event()
    commandReady = threading.Event()
    
    #work queue and result queue, respectively
    sensorQueue = Queue.Queue()
    commandQueue = Queue.Queue()
    reportQueue = Queue.Queue()
    
    # spawn threads
    print "Spawning threads"
    sensor= SensorThread(0, sensorStop, go, resume, sensorQueue)
    robo = RobotThread(resume, sensorStop, go, commandReady, commandQueue, sensorQueue)
    readThread = dataReadPi(ready = receiveReady, waiting = sensorStop, retQueue = commandQueue, host = '')
    sendThread = dataSendPi(ready = sendReady, waiting = sensorStop, sensorQueue = sensorQueue, host = '')
    sensor.start()
    robo.start()
    readThread.start()
    #not sure but may help synchronize socket binding in read events
    receiveReady.wait()
    receiveReady.clear()
    sendThread.start()
    try:
        while True:
            #try to read a command from robotThread
            go.set()
        # if obstacle is detected, get sensor reading which triggered obstacle detection
            while (sensorStop.isSet()):
                go.clear()
                #send information to console to notify that robot has had to stop.
                #update console of state
                sendReady.set()
                # Wait for continue event to be set from robot thread
                resume.wait()
                #senseRead = sensorQueue.get()
                #print "Sensor reads: " + str(senseRead)
                # clear stop to end loop and allow threads to resume duties
                sensorStop.clear()
                #continue

            if not sensorStop.isSet() and receiveReady.isSet():
                if not commandQueue.empty():
                    commandReady.isSet()
                continue
            
    except KeyboardInterrupt:
        go.clear()
        sensorStop.clear()
        print "Keyboard interrupt detected"
        
    print "Joining threads."
    sensor.join()
    robo.join()
    readThread.join()
    sendThread.join()
    return


if __name__ == '__main__':
    import sys
    main()
    print "End of file"
    sys.exit()
