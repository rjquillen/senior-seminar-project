# client socket
# control robot through this client on pi's server

import socket
import Tkinter as tk

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host="136.227.194.227"     # IP address (changes- not static)
port=8000

s.connect((host,port))
    
def key(event):

    if event.keysym=='Escape':
        s.send('EXIT')
        print "Ending program"
        s.close()
        root.destroy()
        return
    else:
        s.send(str(event.char))
        print event.char

root=tk.Tk()
print ("Use the keyboard to control the robot (ESCAPE to exit)")
root.bind_all('<Key>', key)
root.mainloop()
