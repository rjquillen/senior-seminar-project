# read path from file made by writePath.py and travel along path

import time
import myRobotClass as mrc

button_delay=0.1

bob=mrc.Robot()
filename="writepath.txt"

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
        
    # speed down  
    elif direction=="j":
        bob.speeddown()
        time.sleep(button_delay)
        
    # trim right  
    elif direction=="k":
        bob.trimright()
        time.sleep(button_delay)
        
    # trim left
    elif direction=="h":
        bob.trimleft()
        time.sleep(button_delay)

    # reset trim
    elif direction=="r":
        bob.resetTrim()
        time.sleep(button_delay)

    # do nothing
    else:
        time.sleep(button_delay)
        
x=raw_input("press enter to start path")

myfile=open(filename,"r")

data = myfile.readlines()
tmp2=""
for line in data:
    tmp1=str(line).rstrip('\n')
    if not(tmp1==tmp2):
        time.sleep(0.1)
    go(tmp1)
    print(tmp1)
    tmp2=tmp1
    
myfile.close()
