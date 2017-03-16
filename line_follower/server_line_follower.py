import time
import myRobotClass as mrc
from time import sleep
import socket


# set up socket
host=''
port=8000

def setupServer():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print "socket creaded"
    try:
        s.bind((host,port))
    except socket.error as msg:
        print msg
    print "socket bind complete"
    return s

def setupConnection():
    s.listen(1)
    conn, address = s.accept()
    print "connected to : "+address[0]+ ":"+str(address[1])
    return conn

#######################################

button_delay=0.1

bob=mrc.Robot()
bob.setSpeed(100)
        
def dataTransfer(conn):
    
    while True:
        data=conn.recv(1024)

        print str(data)

        if str(data).lower()=='exit':
            s.close()
            print "end of server"
            sleep(1)
            print "end of program"
            break

        if True:

            if str(data).lower()=='forward':
                bob.forward()
                sleep(button_delay)
                bob.stop()

            elif str(data).lower()=='left':
                bob.left()
                sleep(button_delay)
                bob.stop()

            elif str(data).lower()=='right':
                bob.right()
                sleep(button_delay)
                bob.stop()

            elif str(data).lower()=='right_trim':
                bob.trimright()

            elif str(data).lower()=='left_trim':
                bob.trimleft()

            else:
                print "not a recognized command"
        
    conn.close()

s =setupServer()

while True:
    try:
        conn=setupConnection()
        dataTransfer(conn)

    except:
        break
