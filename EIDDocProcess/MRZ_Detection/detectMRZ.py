import cv2
import imutils
import numpy as np
from analyze_contour_detection import getRoiForContours
from cropRoiImage import cropRoiImages

import os
import glob


__IMAGE_CONST_RESIZE__ = 1000



def resizeMinAreaRect(rect, transRatio):

    ref_rect = []
    print rect
    c_x, c_y = rect[0]
    w, h = rect[1]
    ag = rect[2]
    ref_rect.append((float(c_x) * transRatio , float(c_y) * transRatio))
    ref_rect.append((float(w) * transRatio , float(h) * transRatio ))
    ref_rect.append(ag)

    return tuple(ref_rect)


def resizeMRZRects(MRZRects, transRatio):

    ref_MRZRects = []

    for rect in MRZRects:
        rect = resizeMinAreaRect(rect, transRatio)
        ref_MRZRects.append(rect)

    return ref_MRZRects


def detectMRZRoi(image):

    # Reshape image to optimize contour detection
    orig_Height, orig_Width = image.shape[:2]
    image = imutils.resize(image, height=__IMAGE_CONST_RESIZE__)
    chng_Height, chng_Width = image.shape[:2]

    # convert Image to GrayScale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("Image", gray)
    # cv2.waitKey(0)

    # Binarize image using adaptive thresholding
    thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)[1] #cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
    #
    # thresh = cv2.erode(thresh, None, iterations=1)

    # Invert Image
    thresh = cv2.bitwise_not(thresh)


    # cv2.imshow("Image", thresh)
    # cv2.waitKey(0)

    all_MRZ_Potential_Rects = []

    # Loop over to dilate value to find the best match
    for dilateVal in xrange(1,8):

        # Dilate image iteratively to get the MRZ line connected together
        # thresh = cv2.erode(thresh, None, iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=dilateVal)

        # show the output images
        # cv2.imshow("Image", thresh)
        # cv2.waitKey(0)


        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # Detect contours selection and filter them with the MRZ properties
        MRZRects = getRoiForContours(cnts, image)

        # Resize MRZ detected rectangles with respect to the original image size and get the angle of the rectangles
        MRZRects = resizeMRZRects(MRZRects, float(orig_Height)/chng_Height)

        if not len(MRZRects) == 0:

            print "Potential MRZ found"
            all_MRZ_Potential_Rects += MRZRects

    return all_MRZ_Potential_Rects




# Input : OpenCV Image : Raw Coloured image of Passport
# Output : OpenCV Image, OpenCV Image, Validity : Cropped MRZ Section, Cropped Passport ROI, Confirmation document is a passport.
def getMRZ_ROI(cvImage):

    # Get list of minAreaRects containing the pair of ROIs of MRZ Section
    MRZRects = detectMRZRoi(cvImage)

    if MRZRects is None:

        return []

    else:

        return cropRoiImages(cvImage, MRZRects)

#
# os.chdir("/Users/naunidhsingh/Desktop/HSBC/docs/eid")
#
# for img in glob.glob("*.jpg"):
#
#     cvimage = cv2.imread("/Users/naunidhsingh/Desktop/HSBC/docs/eid/" + img)
#     print img
#     mrzImages = getMRZ_ROI(cvimage)
#
#     for mrzImage in mrzImages:
#         cv2.imshow("img", mrzImage)
#         cv2.waitKey()


    # if mrzImage is not None:
    #     cv2.imwrite("MRZ_" + img, mrzImage)