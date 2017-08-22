import cv2
import numpy as np
from VisaDocProcess.detectROI.Barcode import getBarcodeBox
from FaceDetection import face_detection
import math


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


def rotateImage(cvImage, angle):

    (h, w) = cvImage.shape[:2]
    center = (w // 2, h // 2)

    rMat = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotatedImage = cv2.warpAffine(cvImage, rMat, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotatedImage

def getRotatedPoint(points, rotationMatrix):
    # # points
    ones = np.ones(shape=(len(points), 1))
    points_ones = np.hstack([points, ones])
    # transform points
    transformed_points = rotationMatrix.dot(points_ones.T).T
    transformed_points += (0.5)
    transformed_points = transformed_points.astype(int)
    # transformed_points.sort()
    try:
        return transformed_points
    except:
        print "Problem here"
        return None


def getCentreOfRect(rect):

    x_centre, y_centre = np.sum(rect, axis=0)/4

    return x_centre, y_centre

def getRectAvgSide(rect):

    Xs = [i[0] for i in rect]
    Ys = [i[1] for i in rect]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    return (x2-x1+y2-y1)/2


# Get Visa ROI using face detection
# Input : Colored Image (Raw Image Document)
# Output : Coloured Image (Cropped Image containing the ROI as VISA doc only)

def getVisaROI(cvImage):

    if cvImage is None:

        return None

    # Step 1 : get the face detection and barcode detection from the original image
    #          If barcode or face not detected rotate image by 90, barcode works on gradient in x direction so might not get detected if erect at 90 deg
    faceRect = face_detection.getFaceROI(cvImage)
    barcodeRect, angle = getBarcodeBox(cvImage)
    if faceRect is None or barcodeRect is None:
        cvImage = rotateImagePadded(cvImage, -90)
        faceRect = face_detection.getFaceROI(cvImage)
        barcodeRect, angle = getBarcodeBox(cvImage)

        if faceRect is None or barcodeRect is None:
            return None

    # Temp to view the changes
    # cvImageCopy = cvImage.copy()
    # cv2.drawContours(cvImageCopy, [faceRect], -1, (0, 255, 0), 3)
    # cv2.drawContours(cvImageCopy, [barcodeRect], -1, (0, 255, 0), 3)

    # cv2.imshow("Image", cvImageCopy)
    # cv2.waitKey(0)

    # Step 2 : Check the face is above the barcode, as is in the visa
    #          Loop over visa image 4 times checking the orientation on all 4 sides.
    for i in xrange(4):
        faceCentre = getCentreOfRect(faceRect)
        barcodeCentre = getCentreOfRect(barcodeRect)
        faceWidth = getRectAvgSide(faceRect)
        if faceCentre[1] + faceWidth <= barcodeCentre[1]:
            break
        else:
            (h, w) = cvImage.shape[:2]
            center = (w // 2, h // 2)
            rMat = cv2.getRotationMatrix2D(center, 90, 1.0)
            cvImage = rotateImagePadded(cvImage, 90)
            faceRect = getRotatedPoint(faceRect, rMat)
            barcodeRect = getRotatedPoint(barcodeRect, rMat)
            # # Temp to view the changes
            # cvImageCopy = cvImage[:]
            # cv2.drawContours(cvImageCopy, [faceRect], -1, (0, 255, 0), 3)
            # cv2.drawContours(cvImageCopy, [barcodeRect], -1, (0, 255, 0), 3)

            # cv2.imshow("Image", cvImageCopy)
            # cv2.waitKey(0)

    # cv2.drawContours(cvImage, [faceRect], -1, (0, 255, 0), 3)
    # cv2.drawContours(cvImage, [barcodeRect], -1, (0, 255, 0), 3)

    # Step 3 : Again detect the face ROI and the barcode ROI
    #          The face and barcode ROIs may get distorted while rotating the image with padding

    faceRect = getFaceROI(cvImage)
    barcodeRect, angle = getBarcodeBox(cvImage)
    if faceRect is None or barcodeRect is None:
        return None
    #
    # cv2.drawContours(cvImageCopy, [faceRect], -1, (0, 255, 0), 3)
    # cv2.drawContours(cvImageCopy, [barcodeRect], -1, (0, 255, 0), 3)
    # cv2.imshow("Image", cvImage)
    # cv2.waitKey(0)

    # Rotate the Image
    (h, w) = cvImage.shape[:2]
    center = (w // 2, h // 2)
    rMat = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotatedImage = cv2.warpAffine(cvImage, rMat, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


    # Get Rotated Keys for face and barcode
    rotatedFaceRect = getRotatedPoint(faceRect, rMat)
    rotatedBarcodeRect = getRotatedPoint(barcodeRect, rMat)

    # Get Barcode Rect and ROI perspective
    barcodePT_A =  np.min(rotatedBarcodeRect, axis=0)
    barcodePT_B =  np.max(rotatedBarcodeRect, axis=0)
    barcodeRect_width = barcodePT_B[1] - barcodePT_A[1]

    # Get Face Rect and ROI perspective
    facerectPT_A =  np.min(rotatedFaceRect, axis=0)

    # cv2.drawContours(rotatedImage, [rotatedBarcodeRect], -1, (0, 255, 0), 3)
    # cv2.drawContours(rotatedImage, [rotatedFaceRect], -1, (0, 255, 0), 3)

    # Get ROI
    ROI_x1 = int(max( min(barcodePT_A[0], facerectPT_A[0]), 0) + 0.5)
    ROI_x2 = int(min( barcodePT_A[0] + 10*barcodeRect_width, w ) + 0.5)
    ROI_y1 = int(max( min( barcodePT_A[1] - 5*barcodeRect_width, facerectPT_A[1]), 0) + 0.5)
    ROI_y2 = int(min( barcodePT_A[1] + 1.1*barcodeRect_width, h) + 0.5)

    croppedImage = rotatedImage[ROI_y1: ROI_y2, ROI_x1: ROI_x2]

    return croppedImage

    # cv2.drawContours(rotatedImage, [rotatedBarcodeRect], -1, (0, 255, 0), 1)
    # cv2.imshow("Image", croppedImage)
    # cv2.waitKey(0)


# path = "/Users/naunidhsingh/Desktop/HSBC/docs/visa"
#
# os.chdir(path)
# for fil in glob.glob("W0010 copy.png"):
#     img = cv2.imread(fil)
#     if img is not None:
#         getVisaROI(img)
