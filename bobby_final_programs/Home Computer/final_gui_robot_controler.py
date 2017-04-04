# Control raspberry pi robot through this gui on home computer
#
# 1. Set-ups: gui, sockets (receive and send)
# 2. Threads: image updater, sonar updater
# 3. Process gui buttons
#       - line follow
#       - keyboard command
#       - button command
#       - exit
# 4. Exit: send end command, close all sockets, close connections, stop all threads, close gui window, exit program
#

##### Imports #####
from Tkinter import *
from PIL import ImageTk, Image
import Tkinter as tk
import urllib
import socket
import threading
import time
from process_image_function2 import *

##### Constants #####
host = '136.227.194.172'
command_port = 8000
sonar_port = 8001
path = "urlimage.jpg"
url = "http://136.227.194.172/cam_pic.php?time=1491337607178&pDelay=40000"
line_follow_delay=0.1
send_delay=0.05
thread_delay=0.04

###### Globals ######
running = True
line_follow=False

##### Functions ######

# Update Image Function
def update_image():
    global panel
    global running

    while running:
        try:
            global path
            global url
            urllib.urlretrieve(url, path)
            img = ImageTk.PhotoImage(Image.open(path).resize((300, 300), Image.ANTIALIAS))
            panel.configure(image=img)
            panel.image = img
        except:
            print "no new image"
        time.sleep(thread_delay)

# Update Sonar Function
def update_sonar():
    while running:
        data=sonar_socket.recv(1024)
        data="Sonar Distance = "+str(data)
        sonar_var.set(data)
        time.sleep(thread_delay)

# Function for KeyBoard Control
def key(event):
    global radiobutton_var
    global running
    if radiobutton_var.get() == 1:
        if event.keysym == 'Escape':
            command_socket.send('EXIT')
            running = False
            print "Ending program"
            command_socket.close()
            root.destroy()
            return
        else:
            command_socket.send(str(event.char))
            print event.char
        time.sleep(send_delay)

# Function for Line Follower
def send_directions():
    try:
        direction = process_image(path)

        if direction[0] == "left":
            if direction[1] == "veer left":
                command_socket.send("w")
            else:
                command_socket.send('a')
        elif direction[0] == "right":
            if direction[1] == "veer right":
                command_socket.send("w")
            else:
                command_socket.send('d')
        elif direction[0] == "straight" or direction[0] == "no1" or direction[0] == "no2":
            if direction[1] == "veer right":
                command_socket.send('d')
            elif direction[1] == "veer left":
                command_socket.send('a')
            else:
                command_socket.send('w')
        else:
            command_socket.send("bad_image")

    except:
        print "image processing didn't work"

# Line Follow Function that will be threaded to continue
def start_line_follow():
    global line_follow

    while line_follow:
        send_directions()
        time.sleep(line_follow_delay)

# Function for RadioButton Presses
def sel():
    global radiobutton_var
    global line_follow

    if radiobutton_var.get() == 2:
        line_follow = True
        line_thread = threading.Thread(target=start_line_follow)
        line_thread.start()
    else:
        line_follow = False

# Directional Button Functions
def up_button():
    command_socket.send('w')
    time.sleep(send_delay)
def down_button():
    command_socket.send('s')
    time.sleep(send_delay)
def right_button():
    command_socket.send('d')
    time.sleep(send_delay)
def left_button():
    command_socket.send('a')
    time.sleep(send_delay)

# Exit Button Function
def end_program():
    global running

    command_socket.send('EXIT')
    running = False
    print "Ending program"
    command_socket.close()
    time.sleep(1)
    root.destroy()

##### Run code #####

# 1 Set-ups

# Set up gui
root = Tk()
root.title("Senior Seminar")
root.geometry("620x480")
radiobutton_var = IntVar()
radiobutton_var.set(1)  # initializing the choice

leftFrame = Frame(root)
leftFrame.pack(side=LEFT)

rightFrame = Frame(root)
rightFrame.pack(side=RIGHT)

exitButton = Button(rightFrame, text="Exit", command=end_program, width=10)
keyControl = Radiobutton(rightFrame, text="Keyboard Control", variable=radiobutton_var, value=1, command=sel)
followLine = Radiobutton(rightFrame, text="Follow Line", variable=radiobutton_var, value=2, command=sel)
stopRobot = Radiobutton(rightFrame, text="Stop Robot", variable=radiobutton_var, value=3, command=sel)

sonar_var=StringVar()
sonar_var.set("Sonar Distance = Not Received Yet")

sonarLabel = Label(rightFrame, textvariable = sonar_var)
sonarNumbers = Label(rightFrame, text="", bg="black", fg="white")
buttonForward = Button(rightFrame, text="Forward", command=up_button, width=10)
buttonLeft = Button(rightFrame, text="Left", command=left_button, width=10)
buttonRight = Button(rightFrame, text="Right", command=right_button, width=10)
buttonBackwards = Button(rightFrame, text="Backwards", command=down_button, width=10)

exitButton.grid(row=1, column=1, columnspan=3, sticky=W)
keyControl.grid(row=2, column=1, columnspan=3, sticky=W)
followLine.grid(row=3, column=1, columnspan=3, sticky=W)
stopRobot.grid(row=4, column=1, columnspan=3, sticky=W)

sonarLabel.grid(row=5, column=1, columnspan=2)
sonarNumbers.grid(row=5, column=3)
buttonForward.grid(row=6, column=2, sticky=N)
buttonLeft.grid(row=7, column=1, sticky=W)
buttonRight.grid(row=7, column=3, sticky=E)
buttonBackwards.grid(row=7, column=2, sticky=S)

image = Image.open("raspberry.jpg")         # image place holder until image retrieval
image = image.resize((300, 300), Image.ANTIALIAS)  # The (300, 300) is (height, width)
img = ImageTk.PhotoImage(image)
panel = tk.Label(leftFrame, image=img)
panel.grid(row=1, column=1)

# Set up Sockets
command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sonar_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

command_socket.connect((host, command_port))
sonar_socket.connect((host, sonar_port))

# 2 Threads

# image updater thread
image_thread=threading.Thread(target=update_image)
image_thread.start()

# sonar updater thread
sonar_thread = threading.Thread(target=update_sonar)
sonar_thread.start()

# 3 Process Gui Buttons

# Start GUI window and use events to control
# button functions defined above
root.bind_all('<Key>', key)
root.mainloop()

# 4 Exit

# end on 'Exit' Button click or 'Esc' in keyboard mode
# end print statement when over
print "End of Program"
