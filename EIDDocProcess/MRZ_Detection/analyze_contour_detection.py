import cv2
import numpy as np
from checkMinAreaRect import inspect_roi_for_contours

__MRZ_MAX_DIM_RATIO__ = 4
__MRZ_MIN_DIM_RATIO__ = 5.5



def getRoiForContours(cnts, image):
    # loop over the contours
    # Get potential mrz rectangles
    doc_min_side_thrsh = min(image.shape[:2])/2
    potential_rects = []

    if image.shape >2:
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        grayImage = image

    for c in cnts:
        # compute the bounding box of the contour and use the contour to
        # compute the aspect ratio and coverage ratio of the bounding box
        # width to the width of the image
        rect = cv2.minAreaRect(c)
        try:
            max_side = float(max(rect[1]))

            sides_ratio = max_side / min(rect[1])
            if sides_ratio > __MRZ_MAX_DIM_RATIO__ and sides_ratio < __MRZ_MIN_DIM_RATIO__ and max_side >= doc_min_side_thrsh:
                if inspect_roi_for_contours(grayImage, c):
                    potential_rects.append(rect)

                # copyImage = image
                # box = np.int0(cv2.cv.BoxPoints(rect))
                # cv2.drawContours(copyImage, [box], -1, (0, 255, 0), 3)
                # cv2.imshow("Image", copyImage)
                # cv2.waitKey(0)

        except:
            print rect
            print "divide by zero"

    return potential_rects
