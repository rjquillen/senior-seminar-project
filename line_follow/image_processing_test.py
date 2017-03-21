import cv2

im_gray = cv2.imread('lineimage.jpg',0)

(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

thresh = 50 # adjust for preference
im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

#im_bw=cv2.flip(im_bw,1)

y,x=im_gray.shape

midpoint=0
midpoint2=0

print "x = "+str(x)
print "y = "+str(y)

y1=y/2+int(y*.15)
y2=y/2-int(y*.15)
yseg=int(y*.3)

def average_white(yval,xval):
    mysum=0
    length=int(x*.05)    
    for z in range(length):
        if (xval+z)<x:
            mysum=mysum+im_bw[yval,xval+z]
        else:
            length=z
            break
    myav=mysum/length
    if myav>100:
        print "\naverage is white\n"
        return True
    print "\naverage is black\n"
    return False
        
# get first lower line
start=True
for z in range(x):
    pix=im_bw[y1,z]
    if pix==0 and start:
        start_pix=z
        print "start black : "+ str(start_pix)
        start=False
    elif pix>0 and not(start):
        if average_white(y1,z):
            end_pix=z
            print "end black : "+str(end_pix)
            start=True
            length=end_pix-start_pix
            if length>int(x*.10):
                print "length of line1 = "+str(length)
                midpoint=start_pix+(length/2)
                print "midpoint1 at : "+str(midpoint)
                break
            
    im_bw[y1,z]=150

# higher line
start=True
for z in range(x):
    pix=im_bw[y2,z]
    if pix==0 and start:
        start_pix2=z
        print "start black : "+ str(start_pix2)
        start=False
    elif pix>0 and not(start):
        if average_white(y2,z):
            end_pix2=z
            print "end black : "+str(end_pix2)
            start=True
            length2=end_pix2-start_pix2
            if length2>int(x*.10):
                print "length of line2 = "+str(length2)
                midpoint2=start_pix2+(length2/2)
                print "midpoint2 at : "+str(midpoint2)
                break
    im_bw[y2,z]=150

# analize
if midpoint>0 and midpoint2>0:
    print
    im_bw[y1,midpoint]=255
    im_bw[y2,midpoint2]=255
    xseg=abs(midpoint-midpoint2)

    if xseg>int(yseg*.25):
        if midpoint2>midpoint:
            print "turning right"
        else:
            print "turning left"
    else:
        print "go straight"
    
    if (midpoint>int(x/2+x*.2) and midpoint2>int(x/2+x*.2)):
        print "on the left side of line --- make left wheel faster/ right wheel slower"
    elif (midpoint<int(x/2-x*.2) and midpoint2<int(x/2-x*.2)):
        print "on the right side of line --- make right wheel faster/ left wheel slower"
    else:
        print "on the line"

elif midpoint>0:
    print " no midpoint 2 "
    if (midpoint>int(x/2+x*.2) ):
        print "on the left side of line --- make left wheel faster/ right wheel slower"
    elif (midpoint<int(x/2-x*.2)):
        print "on the right side of line --- make right wheel faster/ left wheel slower"
    else:
        print "on the line"

elif midpoint2>0:
    print " no midpoint 1 "
    if (midpoint2>int(x/2+x*.2) ):
        print "on the left side of line --- make left wheel faster/ right wheel slower"
    elif (midpoint2<int(x/2-x*.2)):
        print "on the right side of line --- make right wheel faster/ left wheel slower"
    else:
        print "on the line"
else:
    print "no midpoints"

for z in range(y):
    im_bw[z,x/2]=150

cv2.imshow("bw",im_bw)
cv2.imshow("gray scale",im_gray)

cv2.waitKey()
cv2.destroyAllWindows()
