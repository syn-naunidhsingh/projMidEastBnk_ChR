import cv2
import numpy as np
import argparse


def getBarcodeBox(image):

    try:
        # load the image and convert it to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # compute the Scharr gradient magnitude representation of the images
        # in both the x and y direction
        gradX = cv2.Sobel(gray, ddepth = cv2.cv.CV_32F, dx = 1, dy = 0, ksize = -1)
        gradY = cv2.Sobel(gray, ddepth = cv2.cv.CV_32F, dx = 0, dy = 1, ksize = -1)

        # subtract the y-gradient from the x-gradient
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)

        # blur and threshold the image
        blurred = cv2.blur(gradient, (7, 8))
        (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)


        # construct a closing kernel and apply it to the thresholded image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # perform a series of erosions and dilations
        closed = cv2.erode(closed, None, iterations = 4)
        closed = cv2.dilate(closed, None, iterations = 4)

        # find the contours in the thresholded image, then sort the contours
        # by their area, keeping only the largest one
        (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

        # compute the rotated bounding box of the largest contour
        rect = cv2.minAreaRect(c)

        # Barcode Check for Visa Barcode structure
        wid = max(rect[1])
        hth = min(rect[1])
        c_ratio = float(wid)/hth
        if c_ratio > 1 and c_ratio < 7:

            # Get angle of rotation
            angle = rect[-1]
            if angle < -45:
                angle = (90 + angle)
            else:
                angle = angle

            box = np.int0(cv2.cv.BoxPoints(rect))

            return box, angle

        else:
            print "Visa Barcode Not present"
            return None, None

    except Exception, e:
        print e
        print "Unable to find the barcode"
        return None, None
# draw a bounding box arounded the detected barcode and display the
# image

# #
#
# img = cv2.imread("/Users/naunidhsingh/Desktop/HSBC/docs/visa/W0009.png")
#
# img = cv2.imread("/Users/naunidhsingh/Desktop/HSBC/docs/visa/photo2.jpg")
#
# print getBarcodeBox(img)


#
# cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
# cv2.imshow("Image", image)
# cv2.waitKey(0)