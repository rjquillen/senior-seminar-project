# RedBallTracker.py

import cv2
import numpy as np
import os


###################################################################################################
def main():
    filename = "red1.jpg"

    imgOriginal = cv2.imread(filename)  # read frame

    if imgOriginal is None:  # if frame was not read successfully
        print "error: frame not read right\n"  # print error message to std out
        os.system("pause")  # pause until user presses a key so user can see error message
        return  # exit while loop (which exits program)

    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(imgHSV, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(imgHSV, lower_red, upper_red)

    mask = mask1 + mask2
    output_img = imgOriginal.copy()
    output_img[np.where(mask == 0)] = 0

    output_hsv = imgHSV.copy()
    output_hsv[np.where(mask == 0)] = 0

    cv2.namedWindow("red 1", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("red 2", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("original", cv2.WINDOW_AUTOSIZE)

    cv2.imshow("red 1", output_hsv)
    cv2.imshow("red 2", output_img)
    cv2.imshow("original", imgOriginal)

    #######################################

    im_gray= cv2.cvtColor(output_hsv,cv2.COLOR_BGR2GRAY )
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    thresh = 75  # adjust for preference
    im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

    im_bw=abs(255-im_bw)
    
    cv2.imshow("bw", im_bw)
    cv2.imshow("gray scale", im_gray)

    #######################################

    cv2.waitKey()
    cv2.destroyAllWindows()

    return


###################################################################################################
if __name__ == "__main__":
    main()
