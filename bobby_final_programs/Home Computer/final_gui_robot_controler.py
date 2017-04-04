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

##### Constants #####
host = '136.227.192.101'
command_port = 8000
sonar_port = 8001
path = "urlimage.jpg"
url = "http://weknowyourdreams.com/images/robot/robot-07.jpg"

###### Globals ######
running = True

##### Functions ######

# Radio Button Function
def sel():
    return

# Button Functions
def test():
    return

# Exit Button Function
def end_program():
    global running

    running=False
    root.destroy()

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

# Update Sonar Function
def update_sonar():
    data=sonar_socket.recv(1024)
    data="Sonar Distance = "+str(data)
    sonar_var.set(data)
    #root.update_idletasks()

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
buttonForward = Button(rightFrame, text="Forward", command=test, width=10)
buttonLeft = Button(rightFrame, text="Left", command=test, width=10)
buttonRight = Button(rightFrame, text="Right", command=test, width=10)
buttonBackwards = Button(rightFrame, text="Backwards", command=test, width=10)

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

image_thread=threading.Thread(target=update_image)
image_thread.start()

sonar_thread = threading.Thread(target=update_sonar)
sonar_thread.start()

root.mainloop()

print "End of Program"
