# Extract Roi With Only text present

import cv2

__MARG__ = 1

import ImageEnhance as ie

def getSideTextCrop(ls_Hist, mean_ratio=0.3):
    side_Start, side_End = 0, len(ls_Hist)

    mean_Hist = float(ls_Hist.sum() / side_End) * mean_ratio

    for x in xrange(len(ls_Hist)):

        if ls_Hist[x] > mean_Hist:
            side_Start = x
            break

    for x in xrange(len(ls_Hist) - 1, -1, -1):

        if ls_Hist[x] > mean_Hist:
            side_End = x
            break

    return side_Start, side_End

def getImageTextRect(img, threshold=127):

    img = ie.grayImage(img)

    img = ie.invertGrayImage(img)

    # length, breadth = img.shape[:2]

    # length_Start, length_End, breadth_Start, breadth_End = 0, length, 0, breadth

    img[img < threshold] = 0

    length_Hist = img.sum(axis=1)

    breadth_Hist = img.sum(axis=0)

    length_Start, length_End = getSideTextCrop(length_Hist)

    breadth_Start, breadth_End = getSideTextCrop(breadth_Hist)

    return length_Start, length_End, breadth_Start, breadth_End
#
#
# def getImageCropped(img, threshold=127):
#     orig_img = imageEnh(img)
#     l,b = orig_img.shape[:2]
#     length_Start, length_End, breadth_Start, breadth_End = getImageTextRect(orig_img, threshold)
#
#     croppedImage = orig_img[max(length_Start-__MARG__, 0):min(length_End+__MARG__, l), max(breadth_Start-__MARG__, 0):min(breadth_End-__MARG__,b)]
#
#     return croppedImage


def getPassportRect(ppimg, threshold = 127):

    orig_img = ie.imageEnh(ppimg)
    l,b = orig_img.shape[:2]
    length_Start, length_End, breadth_Start, breadth_End = getImageTextRect(orig_img, threshold)

    croppedImage = orig_img[max(length_Start-__MARG__, 0):min(length_End+__MARG__, l), max(breadth_Start-__MARG__, 0):min(breadth_End-__MARG__,b)]

    # ie.displayImage(croppedImage)

    return croppedImage
