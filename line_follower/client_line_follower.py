# client socket
# control robot through this client on pi's server

import socket
import urllib
import cv2
from time import sleep

time_delay=0.10

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host="192.168.1.19"     # IP address (changes- not static)
port=8000
url=""       # get image url address
save_address="C:/Users/bobby_000/Desktop/pi_project/test_image.jpg" # place to save image

s.connect((host,port))

def process_image():
    im_gray = cv2.imread(save_address,0)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    thresh = 50 # adjust for preference
    im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
    y,x=im_gray.shape
    y1=y/2+int(y*.15)
    y2=y/2-int(y*.15)
    yseg=int(y*.3)

    # get first lower line
    start=True
    for z in range(x):
        pix=im_bw[y1,z]
        if pix==0 and start:
            start_pix=z
            print "start black : "+ str(start_pix)
            start=False
        elif pix>0 and not(start):
            end_pix=z
            print "end black : "+str(end_pix)
            start=True
            length=end_pix-start_pix
            if length>int(x*.15):
                print "length of line1 = "+str(length)
                midpoint=start_pix+(length/2)
                print "midpoint1 at : "+str(midpoint)
                break

    # higher line
    start=True
    for z in range(x):
        pix=im_bw[y2,z]
        if pix==0 and start:
            start_pix2=z
            print "start black : "+ str(start_pix2)
            start=False
        elif pix>0 and not(start):
            end_pix2=z
            print "end black : "+str(end_pix2)
            start=True
            length2=end_pix2-start_pix2
            if length2>int(x*.15):
                print "length of line2 = "+str(length2)
                midpoint2=start_pix2+(length2/2)
                print "midpoint2 at : "+str(midpoint2)
                break
    print
    im_bw[y1,midpoint]=255
    im_bw[y2,midpoint2]=255
    xseg=abs(midpoint-midpoint2)
    
    if (midpoint>int(x/2+x*.2) and midpoint2>int(x/2+x*.2)):
        print "on the right side of line --- make right wheel faster/ left wheel slower"
        s.send('left_trim')
    elif (midpoint<int(x/2-x*.2) and midpoint2<int(x/2-x*.2)):
        print "on the left side of line --- make left wheel faster/ right wheel slower"
        s.send('right_trim')
    else:
        print "on the line"

    if xseg>int(yseg*.25):
        if midpoint2>midpoint:
            print "turning right"
            s.send('right')
        else:
            print "turning left"
            s.send('left')
    else:
        print "go straight"
        s.send('foward')

while True:
    urllib.urlretrieve(url,save_address)
    process_image()
    sleep(time_delay)   # maybe turnoff if laggy

s.send('EXIT')
print "Ending program"
s.close()
