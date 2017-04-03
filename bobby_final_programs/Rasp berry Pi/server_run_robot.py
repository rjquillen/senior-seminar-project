# run robot through socket

import time
import myRobotClass as mrc
from time import sleep
import socket

# set up socket
host = ''
port = 8000


def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "socket creaded"
    try:
        s.bind((host, port))
    except socket.error as msg:
        print msg
    print "socket bind complete"
    return s


def setupConnection():
    s.listen(1)
    conn, address = s.accept()
    print "connected to : " + address[0] + ":" + str(address[1])
    return conn


#######################################

button_delay = 0.1

bob = mrc.Robot()


def dataTransfer(conn):
    while True:
        data = conn.recv(1024)

        print str(data)

        if str(data).lower() == 'exit':
            s.close()
            print "end of server"
            sleep(1)
            print "end of program"
            break

        if str(data).lower() == 's':
            bob.backward()
            sleep(button_delay)
            bob.stop()

        if True:

            if str(data).lower() == 'w':
                bob.forward()
                sleep(button_delay)
                bob.stop()

            elif str(data).lower() == 'a':
                bob.left()
                sleep(button_delay)
                bob.stop()

            elif str(data).lower() == 'd':
                bob.right()
                sleep(button_delay)
                bob.stop()

            elif str(data).lower() == 'q':
                bob.pivleft()
                sleep(button_delay)
                bob.stop()

            elif str(data).lower() == 'e':
                bob.pivright()
                sleep(button_delay)
                bob.stop()

            else:
                print "not a movement comand"

    conn.close()


s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)

    except:
        break