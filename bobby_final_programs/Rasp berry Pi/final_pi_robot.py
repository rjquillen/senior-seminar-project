# socket server ran robot
#
# 1. set-up: robot from myRobotClass, sonar from SonarClass, receive and send sockets
# 2. start thread: sonar
# 3. on received command run command if sonar data is right
#    and on 'Exit' command end all threads and close all sockets
#

##### Imports ######
import time
import myRobotClass as mrc
from SonarClass import Sonar
from time import sleep
import socket
import threading

##### Constants #####
button_delay=0.03
host = ''
command_port = 8000
sonar_port = 8001
sonar_check=True
running=True

##### Functions #####

# socket functions
def setupServer(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "socket creaded"
    try:
        s.bind((host, port))
    except socket.error as msg:
        print msg
    print "socket bind complete"
    return s

def setupConnection(s):
    s.listen(1)
    conn, address = s.accept()
    print "connected to : " + address[0] + ":" + str(address[1])
    return conn

# sonar function
def check_sonar():
    global running
    global sonar_check
    global sonar_conn
    global sonar_s
    global sue

    while running:
        dist=sue.distance()
        sonar_conn.send(dist)
        if dist<15:
            sonar_check=False
        else:
            sonar_check=True
        time.sleep(0.2)
    sonar_s.close()
    sonar_conn.close()
    print "end of send socket"

# process command function
def process_command(conn):
    global sonar_check
    global running
    global command_s
    global bob

    while True:
        data = conn.recv(1024)

        print str(data)

        if str(data).lower() == 'exit':
            command_s.close()
            print "end of receive socket"
            running=False
            sleep(1)
            break

        if str(data).lower() == 's':
            bob.backward()
            sleep(button_delay)
            bob.stop()

        if sonar_check:

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

    conn.close()

##### Run code #####

# 1 Set-ups

# set up robot
bob = mrc.Robot()

# set up sonar
sue = Sonar()

# set up sockets
command_s = setupServer(command_port)
sonar_s = setupServer(sonar_port)

while True:
    try:
        command_conn = setupConnection(command_s)
        sonar_conn = setupConnection(sonar_s)

        # 2. Thread

        # sonar thread
        sonar_thread = threading.Thread(target=check_sonar)
        sonar_thread.start()

        # 3. Commands

        # process commands and end on 'Exit'
        process_command(command_conn)

    except:
        break

print "end of program"