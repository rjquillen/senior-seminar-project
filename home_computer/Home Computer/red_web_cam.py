# RedBallTracker.py

import cv2
import numpy as np
import os

###################################################################################################
def main():

    capWebcam = cv2.VideoCapture(0)                     # declare a VideoCapture object and associate to webcam, 0 => use 1st webcam

    if capWebcam.isOpened() == False:                           # check if VideoCapture object was associated to webcam successfully
        print "error: capWebcam not accessed successfully\n\n"          # if not, print error message to std out
        os.system("pause")                                              # pause until user presses a key so user can see error message
        return                                                          # and exit function (which exits program)

    while cv2.waitKey(1) != 27 and capWebcam.isOpened():                # until the Esc key is pressed or webcam connection is lost
        blnFrameReadSuccessfully, imgOriginal = capWebcam.read()            # read next frame

        if not blnFrameReadSuccessfully or imgOriginal is None:             # if frame was not read successfully
            print "error: frame not read from webcam\n"                     # print error message to std out
            os.system("pause")                                              # pause until user presses a key so user can see error message
            break                                                           # exit while loop (which exits program)

        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

        imgThreshLow = cv2.inRange(imgHSV, (0, 155, 155), (18, 255, 255))
        imgThreshHigh = cv2.inRange(imgHSV, (165, 155, 155), (179, 255, 255))

        imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

        imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)                 # blur

        imgThresh = cv2.dilate(imgThresh, np.ones((5,5),np.uint8))        # close image (dilate, then erode)
        imgThresh = cv2.erode(imgThresh, np.ones((5,5),np.uint8))         # closing "closes" (i.e. fills in) foreground gaps

        ######################################################
        lower_red=np.array([0,50,50])
        upper_red=np.array([10,255,255])
        mask1=cv2.inRange(imgHSV,lower_red,upper_red)

        lower_red=np.array([170,50,50])
        upper_red=np.array([180,255,255])
        mask2=cv2.inRange(imgHSV,lower_red,upper_red)

        mask=mask1+mask2
        output_img=imgOriginal.copy()
        output_img[np.where(mask==0)]=0

        output_hsv=imgHSV.copy()
        output_hsv[np.where(mask==0)]=0

        output_hsv = cv2.GaussianBlur(output_hsv, (3, 3), 2)  # blur
        output_hsv = cv2.dilate(output_hsv, np.ones((5, 5), np.uint8))  # close image (dilate, then erode)
        output_hsv = cv2.erode(output_hsv, np.ones((5, 5), np.uint8))

        output_img = cv2.GaussianBlur(output_img, (3, 3), 2)  # blur
        output_img = cv2.dilate(output_img, np.ones((5, 5), np.uint8))  # close image (dilate, then erode)
        output_img = cv2.erode(output_img, np.ones((5, 5), np.uint8))

        cv2.namedWindow("red 1",cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("red 2",cv2.WINDOW_AUTOSIZE)

        cv2.imshow("red 1",output_hsv)
        cv2.imshow("red 2", output_img)
        ###########################################################

        cv2.namedWindow("imgOriginal", cv2.WINDOW_AUTOSIZE)            # create windows, use WINDOW_AUTOSIZE for a fixed window size
        cv2.namedWindow("imgThresh", cv2.WINDOW_AUTOSIZE)           # or use WINDOW_NORMAL to allow window resizing

        cv2.imshow("imgOriginal", imgOriginal)                 # show windows
        cv2.imshow("imgThresh", imgThresh)

        im_gray = cv2.cvtColor(output_hsv, cv2.COLOR_BGR2GRAY)
        (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        thresh = 75  # adjust for preference
        im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

        im_bw = abs(255 - im_bw)

        cv2.imshow("bw", im_bw)
        cv2.imshow("gray scale", im_gray)

    # end while

    cv2.destroyAllWindows()                     # remove windows from memory

    return

###################################################################################################
if __name__ == "__main__":
    main()
