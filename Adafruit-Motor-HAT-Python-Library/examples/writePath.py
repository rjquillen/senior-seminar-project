# manuelly drive robot with a wii remote and save course on a file
# later read by readPath.py to copycat the path driven

#imports
import cwiid
import time
import myRobotClass as mrc


# constants
filename="writepath.txt"
button_delay=0.1

# set up robot
bob=mrc.Robot()

#connect wii remote
print "press 1 + 2 on your wii remote"
time.sleep(1)
try:
    wii=cwiid.Wiimote()
except:
    print "Error opening wii remote"
    quit()

#go and save to file
def go(direction):

    # forward
    if direction=="w":
        bob.forward()
        time.sleep(button_delay)
        bob.stop()
        
    # backwards  
    elif direction=="s":
        bob.backward()
        time.sleep(button_delay)
        bob.stop()
        
    # left
    elif direction=="a":
        bob.left()
        time.sleep(button_delay)
        bob.stop()
        
    # right 
    elif direction=="d":
        bob.right()
        time.sleep(button_delay)
        bob.stop()
        
    # piv right   
    elif direction=="e":
        bob.pivright()
        time.sleep(button_delay)
        bob.stop()
        
    # piv left  
    elif direction=="q":
        bob.pivleft()
        time.sleep(button_delay)
        bob.stop()
        
    # speed up   
    elif direction=="u":
        bob.speedup()
        time.sleep(button_delay)
        print bob.getspeed()
        
    # speed down  
    elif direction=="j":
        bob.speeddown()
        time.sleep(button_delay)
        print bob.getspeed()
        
    # trim right  
    elif direction=="k":
        bob.trimright()
        time.sleep(button_delay)
        print bob.getspeed()
        
    # trim left
    elif direction=="h":
        bob.trimleft()
        time.sleep(button_delay)
        print bob.getspeed()

    # reset trim
    elif direction=="r":
        bob.resetTrim()
        time.sleep(button_delay)
        print bob.getspeed()

# open file to write
myfile=open(filename,"w")

wii.rpt_mode=cwiid.RPT_BTN

# loop to get buttons 
while True:

    # reset states
    buttons =wii.state['buttons']

    # end program
    if(buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS==0):
        print "closing connection..."
        myfile.close()
        wii.rumble=1
        time.sleep(1)
        wii.rumble=0
        exit(wii)

    # backward
    elif (buttons & cwiid.BTN_LEFT):
        myfile.write("s\n")
        go("s")

    # forward   
    elif (buttons & cwiid.BTN_RIGHT):
        myfile.write("w\n")
        go("w")

    # left
    elif (buttons & cwiid.BTN_UP):
        myfile.write("a\n")
        go("a")

    # right
    elif (buttons & cwiid.BTN_DOWN):
        myfile.write("d\n")
        go('d')
        
    # piv left
    elif (buttons & cwiid.BTN_1):
        myfile.write("q\n")
        go('q')

    # piv right
    elif (buttons & cwiid.BTN_2):
        myfile.write("e\n")
        go('e')

    # increase speed
    elif (buttons & cwiid.BTN_A):
        myfile.write("u\n")
        go("u")

    # decrease speed
    elif (buttons & cwiid.BTN_B):
        myfile.write("j\n")
        go('j')

    # reset trim
    elif (buttons & cwiid.BTN_HOME):
        myfile.write('r\n')
        go('r')
        
    # trim right
    elif (buttons & cwiid.BTN_MINUS):
        myfile.write('k\n')
        go('k')

    # trim left
    elif (buttons & cwiid.BTN_PLUS):
        myfile.write('h\n')
        go('h')
    



        

