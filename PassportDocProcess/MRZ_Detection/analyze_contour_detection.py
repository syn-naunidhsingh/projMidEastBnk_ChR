import cv2
import numpy as np
from SetElement import SetElement


__MRZ_DIM_RATIO__ = float(20)


def get_dist(x,y):
    return np.sqrt(np.sum((np.array(x)-np.array(y))**2))

def compareWidthOfRects(contour_rects):
    widthCompares = []
    for rect in contour_rects:

        if len(widthCompares) == 0:
            wth_comp = SetElement()
            wth_comp.push_element(max(rect[1]), rect)
            widthCompares.append(wth_comp)

        else:
            isInserted = False
            for wth_comp in widthCompares:
                if wth_comp.valid_push_ratio(max(rect[1]), 0.15):
                    wth_comp.push_element(max(rect[1]), rect)
                    isInserted = True

            if not isInserted:
                wth_comp = SetElement()
                wth_comp.push_element(max(rect[1]), rect)
                widthCompares.append(wth_comp)

    return widthCompares


def transformRectBy90(rect):
    # Transform the rect tuples by 90
    new_centre = rect[0]
    new_size = (rect[1][1], rect[1][0])
    new_angle = 90+rect[2]
    return (new_centre, new_size, new_angle)


def compareAngleOfRects(contour_rects):
    angleCompares = []

    for wth_comp in contour_rects:

        currAngleCompares = []

        for rect in wth_comp.datas:

            if len(currAngleCompares) == 0:
                ag_comp = SetElement()
                ag_comp.push_element(rect[2], rect)
                currAngleCompares.append(ag_comp)

            else:
                isInserted = False
                for ag_comp in currAngleCompares:

                    chnged_rect = transformRectBy90(rect)
                    if ag_comp.valid_push_const(rect[2], 0.7):
                        ag_comp.push_element(rect[2], rect)
                        isInserted = True
                    elif ag_comp.valid_push_const(chnged_rect[2], 0.7):
                        ag_comp.push_element(chnged_rect[2], chnged_rect)
                        isInserted = True

                if not isInserted:
                    ag_comp = SetElement()
                    ag_comp.push_element(rect[2], rect)
                    currAngleCompares.append(ag_comp)

        angleCompares += currAngleCompares

    return angleCompares

def analyzeMRZRects(contour_rects):
    MRZ_Rects = []

    for ag_comp in contour_rects:

        if not len(ag_comp.datas) < 2:

            rects = ag_comp.datas
            for i in range(len(rects)):

                for j in range(len(rects)):

                    if i != j:
                        centre_dist = get_dist(rects[i][0], rects[j][0])
                        thresh_dist = 2 * (float(min(rects[i][1])) + float(min(rects[j][1])))
                        if centre_dist < thresh_dist:
                            pair_set = []
                            pair_set.append(rects[i])
                            pair_set.append(rects[j])
                            MRZ_Rects.append(pair_set)

    return MRZ_Rects

def getRoiForContours(cnts, image):
    # loop over the contours
    # Get potential mrz rectangles
    potential_rects = []
    for c in cnts:
        # compute the bounding box of the contour and use the contour to
        # compute the aspect ratio and coverage ratio of the bounding box
        # width to the width of the image
        rect = cv2.minAreaRect(c)
        try:
            if rect[1][0] / rect[1][1] > __MRZ_DIM_RATIO__ or rect[1][0] / rect[1][1] < 1 / __MRZ_DIM_RATIO__:
                potential_rects.append(rect)
                # copyImage = image
                # box = np.int0(cv2.cv.BoxPoints(rect))
                # cv2.drawContours(copyImage, [box], -1, (0, 255, 0), 3)
                # cv2.imshow("Image", copyImage)
                # cv2.waitKey(0)

        except:
            print rect
            print "divide by zero"

            # find MRZ Pair
        # Create sets by comparing length of the rects; assumption - the two mrz lines will have similar length
    widthCompares = compareWidthOfRects(potential_rects)

    angleCompares = compareAngleOfRects(widthCompares)

    MRZ_Rects = analyzeMRZRects(angleCompares)

    return MRZ_Rects