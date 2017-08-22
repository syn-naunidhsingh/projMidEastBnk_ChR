import cv2
import numpy as np
import math
from removeBlackMargin import autocrop

def rotateImagePadded(image, angle):
    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1)

    radians = math.radians(angle)
    sin = math.sin(radians)
    cos = math.cos(radians)
    bound_w = int((height * abs(sin)) + (width * abs(cos)))
    bound_h = int((height * abs(cos)) + (width * abs(sin)))

    rotation_mat[0, 2] += ((bound_w / 2) - image_center[0])
    rotation_mat[1, 2] += ((bound_h / 2) - image_center[1])

    rotated_mat = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h))
    return rotated_mat

def inspect_roi_for_contours(cvImageGray, cnt):

    cvImageBin = cv2.threshold(cvImageGray, 100, 255, cv2.THRESH_BINARY)[1]
    cvImageBin = cv2.bitwise_not(cvImageBin)

    rect = cv2.minAreaRect(cnt)

    mask = np.zeros(cvImageGray.shape, np.uint8)

    cv2.drawContours(mask, [cnt], 0, (255), -1)

    # cv2.imshow("cnt draw", mask)
    #
    # cv2.waitKey()

    res = cv2.bitwise_and(cvImageBin, cvImageBin, mask=mask)


    rotImage = rotateImagePadded(res, rect[-1])

    croppedImage = autocrop(rotImage)
    h,w = croppedImage.shape[:2]
    if h>w:
        croppedImage = rotateImagePadded(croppedImage, 90)

    # cv2.imshow("rect draw", croppedImage)
    # cv2.waitKey()

    length_Hist = croppedImage.sum(axis=1)
    print croppedImage.shape
    print len(length_Hist)
    print length_Hist

    x_field = np.array(range(len(length_Hist)))
    y_field = length_Hist

    try:
        poly = np.polyfit(x_field, y_field, 6)

        y_int = np.polyval(poly, x_field)

        minimas = np.r_[True, y_int[1:] < y_int[:-1]] & np.r_[y_int[:-1] < y_int[1:], True]
        maximas = np.r_[True, y_int[1:] > y_int[:-1]] & np.r_[y_int[:-1] > y_int[1:], True]
        print minimas
        count_minimas = np.count_nonzero(minimas[1:-1])
        count_maximas = np.count_nonzero(maximas)
        if count_minimas == 2 and count_maximas == 3:
            return True
        else:
            return False

    except Exception, e:
        print e
        return False









