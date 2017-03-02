import sys
import time
import myRobotClass as mrc
import Tkinter as tk

bob=mrc.Robot()
    

def key_input(event):
    print "key",event.char
    key_press=event.char
    st=0.030

    if key_press.lower()=='w':
        bob.forward()
        time.sleep(st)
        bob.stop()
    elif key_press.lower()=='s':
        bob.backward()
        time.sleep(st)
        bob.stop()
    elif key_press.lower()=='a':
        bob.left()
        time.sleep(st)
        bob.stop()
    elif key_press.lower()=='d':
        bob.right()
        time.sleep(st)
        bob.stop()
    elif key_press.lower()=='q':
        bob.stop()
        sys.exit()

command=tk.Tk()
command.bind('<KeyPress>',key_input)
command.mainloop()
