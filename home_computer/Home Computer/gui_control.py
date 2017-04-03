# client socket
# control robot through this client on pi's server
# upload image on tkinter window

import socket
import Tkinter as tk
from PIL import ImageTk, Image
import urllib
from process_image_function import *
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.1.246"  # IP address (changes- not static)
port = 8000

path = "test.jpg"
url = "http://192.168.1.246/html/cam_pic.php?time=1491100140133&pDelay=40000"

s.connect((host, port))


def update_pic():
    global panel
    global new_pic
    while new_pic:
        try:
            global path
            global url
            urllib.urlretrieve(url, path)
            img = ImageTk.PhotoImage(Image.open(path))
            panel.configure(image=img)
            panel.image = img
        except:
            print "no new image"


def key(event):
    global var
    global new_pic

    if var.get() == 1:

        if event.keysym == 'Escape':
            s.send('EXIT')
            new_pic = False
            print "Ending program"
            s.close()
            root.destroy()
            return
        else:
            s.send(str(event.char))
            print event.char


def send_directions():
    global keep_going
    global old

    try:
        # get_url_image(path)
        try:
            direction = process_image(path)

            if direction[0] == "left":
                if direction[1] == "veer left":
                    s.send("w")
                    #            print "sent w"
                    old = "w"
                else:
                    s.send('a')
                    #             print "sent a"
                    old = "a"
            elif direction[0] == "right":
                if direction[1] == "veer right":
                    s.send("w")
                    #              print "sent w"
                    old = "w"
                else:
                    s.send('d')
                    #               print "sent d"
                    old = "d"
            elif direction[0] == "straight" or direction[0] == "no1" or direction[0] == "no2":
                if direction[1] == "veer right":
                    s.send('d')
                    #                print "sent d"
                    old = "d"
                elif direction[1] == "veer left":
                    s.send('a')
                    #                 print "sent a"
                    old = "a"
                else:
                    s.send('w')
                    #                  print "sent w"
                    old = "w"
            else:
                pass
                #               print "can't decide!!! help!\nending programs :("

        except:
            print "image processing didn't work"
    except:
        print "get image didn't work"


def start_line_follow():
    global line_go

    while line_go:
        send_directions()


def sel():
    global var
    global line_go

    if var.get() == 2:
        line_go = True
        line_thread = threading.Thread(target=start_line_follow)
        line_thread.start()
    else:
        line_go = False


line_go = False

root = tk.Tk()
root.title("image")
root.geometry("600x600")
root.configure(background='grey')

urllib.urlretrieve(url, path)
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")

new_pic = True
picthread = threading.Thread(target=update_pic)
picthread.start()

var = tk.IntVar()
R1 = tk.Radiobutton(root, text="keyboard control", variable=var, value=1, command=sel)
R1.pack(anchor=tk.W)
R2 = tk.Radiobutton(root, text="follow line", variable=var, value=2, command=sel)
R2.pack(anchor=tk.W)
R3 = tk.Radiobutton(root, text="stop", variable=var, value=3, command=sel)
R3.pack(anchor=tk.W)

print ("Use the keyboard to control the robot (ESCAPE to exit)")
root.bind_all('<Key>', key)
root.mainloop()
