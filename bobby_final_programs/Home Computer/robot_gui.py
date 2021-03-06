from Tkinter import *
from PIL import ImageTk, Image
import Tkinter as tk
import urllib


def test():
    print("Button Clicked and working")


def key(event):
    """"""


def send_directions():
    """"""


def start_line_follow():
    global line_go


def sel():
    global var
    global line_go


host = "136.227.194.164"  # IP address (changes- not static)
port = 8000

line_go = False
path = "test.jpg"
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Wittenberg_Ward_St_En_11-23-08.jpg/250px-Wittenberg_Ward_St_En_11-23-08.jpg"

root = Tk()
root.title("Senior Seminar")
root.geometry("620x480")
var = IntVar()
var.set(1)  # initializing the choice

leftFrame = Frame(root)
leftFrame.pack(side=LEFT)

rightFrame = Frame(root)
rightFrame.pack(side=RIGHT)

pictureCheck = tk.Checkbutton(rightFrame, text="Continuously Grab Picture")
keyControl = Radiobutton(rightFrame, text="Keyboard Control", variable=var, value=1, command=sel)
followLine = Radiobutton(rightFrame, text="Follow Line", variable=var, value=2, command=sel)
stopRobot = Radiobutton(rightFrame, text="Stop Robot", variable=var, value=3, command=sel)

sonarLabel = Label(rightFrame, text="Sonar Distance: ")
sonarNumbers = Label(rightFrame, text="", bg="black", fg="white")
buttonForward = Button(rightFrame, text="Forward", command=test, width=10)
buttonLeft = Button(rightFrame, text="Left", command=test, width=10)
buttonRight = Button(rightFrame, text="Right", command=test, width=10)
buttonBackwards = Button(rightFrame, text="Backwards", command=test, width=10)

pictureCheck.grid(row=1, column=1, columnspan=3, sticky=W)
keyControl.grid(row=2, column=1, columnspan=3, sticky=W)
followLine.grid(row=3, column=1, columnspan=3, sticky=W)
stopRobot.grid(row=4, column=1, columnspan=3, sticky=W)

sonarLabel.grid(row=5, column=1, columnspan=2)
sonarNumbers.grid(row=5, column=3)
buttonForward.grid(row=6, column=2, sticky=N)
buttonLeft.grid(row=7, column=1, sticky=W)
buttonRight.grid(row=7, column=3, sticky=E)
buttonBackwards.grid(row=7, column=2, sticky=S)

# if checkVariable = True
# Grab image Continuously
# Program thread here

urllib.urlretrieve(url, path)
image = Image.open(path)
image = image.resize((300, 300), Image.ANTIALIAS)  # The (300, 300) is (height, width)
img = ImageTk.PhotoImage(image)
panel = tk.Label(leftFrame, image=img)
panel.grid(row=1, column=1)

root.mainloop()