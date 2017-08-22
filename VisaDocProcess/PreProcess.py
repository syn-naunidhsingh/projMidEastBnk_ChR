import cv2
import numpy as np
import pytesseract
from PIL import Image
from detectROI import roi_detection



# Function to call roi detection and image enhancement
# Input : OpenCV image : Raw Image of the document
# Output : OpenCV image : Cropped ROI image OR None, List of alert message codes
def preProcessROICrop(cvImage):

    alertMesg = []

    croppedImage = None
    try:

        croppedImage = roi_detection.getVisaROI(cvImage)

        if croppedImage is None:

            alertMesg.append(3000)

    except:

        alertMesg.append(0100)

    return croppedImage, alertMesg


def preProcessImageEnhance(cvImage):

    if len(cvImage.shape) > 2:
        cvImageGray = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
        return cvImageGray
    else:
        return cvImage

#
# #
# img = cv2.imread("/Users/naunidhsingh/Desktop/HSBC/docs/visa/image011.jpg")
# crp, al = preProcessROICrop(img)
# cv2.imshow("img", crp)
# cv2.waitKey()




