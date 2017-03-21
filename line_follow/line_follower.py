# client socket
# control robot through this client on pi's server
# line follower with process_image_function 

import socket
from process_image_function import*

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host="192.168.1.123"     # IP address (changes- not static)
port=8000

path="test.jpg"
url="http://192.168.1.123/html/cam_pic.php?time=1489966894315&pDelay=40000"

s.connect((host,port))
    
def send_directions():
    global keep_going
    global old

    try:
        get_url_image(path)
        try:
            direction=process_image(path)

            if direction[0]=="left":
                if direction[1]=="veer left":
                    s.send("w")
                    print "sent w"
                    old="w"
                else:
                    s.send('a')
                    print "sent a"
                    old="a"
            elif direction[0]=="right":
                if direction[1]=="veer right":
                    s.send("w")
                    print "sent w"
                    old="w"
                else:
                    s.send('d')
                    print "sent d"
                    old="d"
            elif direction[0]=="straight" or direction[0]=="no1" or direction[0]=="no2":
                if direction[1]=="veer right":
                    s.send('d')
                    print "sent d"
                    old="d"
                elif direction[1]=="veer left":
                    s.send('a')
                    print "sent a"
                    old="a"
                else:
                    s.send('w')
                    print "sent w"
                    old="w"
            else:
                print "can't decide!!! help!\nending programs :("
                keep_going=False
                s.send('EXIT')
                s.close()
        except:
            print "image processing didn't work"
    except:
        print "get image didn't work"
        
x=raw_input("hit enter to start program")
keep_going=True
old="w"
try:    
    while keep_going:
        send_directions()
except:
    s.send('EXIT')
    s.close()
                    
print "program ended successfully"

