import cv2
import urllib
import numpy as np

def average_white(yval, xval, width):
    global im_bw
    mysum = 0
    length = int(width * .05)

    for z in range(length):
        if (xval + z) < width:
            mysum = mysum + im_bw[yval, xval + z]
        else:
            length = z
            break

    myav = mysum / length
    if myav > 100:
        return True
    return False


def process_image(filename):
    global im_bw
    direction = ["", ""]

    imgOriginal = cv2.imread(filename)

    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(imgHSV, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(imgHSV, lower_red, upper_red)

    mask = mask1 + mask2

    output_hsv = imgHSV.copy()
    output_hsv[np.where(mask == 0)] = 0

    im_gray = cv2.cvtColor(output_hsv, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    thresh = 75  # adjust for preference
    im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

    im_bw = abs(255 - im_bw)

    y, x = im_gray.shape

    midpoint = 0
    midpoint2 = 0

    y1 = y / 2 + int(y * .15)
    y2 = y / 2 - int(y * .15)
    yseg = int(y * .3)

    # get first lower line
    start = True
    for z in range(x):
        pix = im_bw[y1, z]
        if pix == 0 and start:
            start_pix = z
            start = False

        elif (z == x - 1) and not (start):
            end_pix = z
            length = end_pix - start_pix
            midpoint = start_pix + (length / 2)
            break

        elif pix > 0 and not (start):
            if average_white(y1, z, x):
                end_pix = z
                start = True
                length = end_pix - start_pix
                if length > int(x * .10):
                    midpoint = start_pix + (length / 2)
                    break

        im_bw[y1, z] = 150

    # higher line
    start = True
    for z in range(x):
        pix = im_bw[y2, z]
        if pix == 0 and start:
            start_pix2 = z
            start = False

        elif (z == x - 1) and not (start):
            end_pix2 = z
            length2 = end_pix2 - start_pix2
            midpoint2 = start_pix2 + (length2 / 2)
            break

        elif pix > 0 and not (start):
            if average_white(y2, z, x):
                end_pix2 = z
                start = True
                length2 = end_pix2 - start_pix2
                if length2 > int(x * .10):
                    midpoint2 = start_pix2 + (length2 / 2)
                    break
        im_bw[y2, z] = 150

    # analize
    if midpoint > 0 and midpoint2 > 0:
        im_bw[y1, midpoint] = 255
        im_bw[y2, midpoint2] = 255
        xseg = abs(midpoint - midpoint2)

        if xseg > int(yseg * .25):
            if midpoint2 > midpoint:
                direction[0] = "right"
            else:
                direction[0] = "left"
        else:
            direction[0] = "straight"

        if (midpoint > int(x / 2 + x * .2) and midpoint2 > int(x / 2 + x * .2)):
            direction[1] = "veer right"
        elif (midpoint < int(x / 2 - x * .2) and midpoint2 < int(x / 2 - x * .2)):
            direction[1] = "veer left"
        else:
            direction[1] = "on line"

    elif midpoint > 0:
        if (midpoint > int(x / 2 + x * .2)):
            direction[1] = "veer right"
        elif (midpoint < int(x / 2 - x * .2)):
            direction[1] = "veer left"
        else:
            direction[1] = "on line"
        direction[0] = "no2"

    elif midpoint2 > 0:
        if (midpoint2 > int(x / 2 + x * .2)):
            direction[1] = "veer right"
        elif (midpoint2 < int(x / 2 - x * .2)):
            direction[1] = "veer left"
        else:
            direction[1] = "on line"
        direction[0] = "no1"
    else:
        direction = ["", ""]

    for z in range(y):
        im_bw[z, x / 2] = 150

    return direction


def get_url_image(filename):
    urllib.urlretrieve("http://136.227.192.101/cam_pic.php?time=1490291697574&pDelay=40000", filename)


