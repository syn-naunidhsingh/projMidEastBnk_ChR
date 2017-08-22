import cv2
import numpy as np
import math



def rotateImage(image, angle):
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

def rotateAndCropMRZ2(img, rect):
    # rotate img
    angle = rect[2]
    rows, cols = img.shape[0], img.shape[1]
    if angle < -45:
        angle = (90 + angle)
    else:
        angle = angle

    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    img_rot = cv2.warpAffine(img, M, (cols, rows))

    # cv2.imshow("image", img_rot)
    # cv2.waitKey()
    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.cv.BoxPoints(rect)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]
    pts[pts < 0] = 0


    Xs = [i[0] for i in pts]
    Ys = [i[1] for i in pts]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)

    # crop
    img_crop = img_rot[y1:y2,
               x1:x2]

    # cv2.imshow("image", img_crop)
    # cv2.waitKey()

    h,w = img_crop.shape[:2]
    if h>w:
        img_crop = rotateImage(img_crop, -90)

    return img_crop

def padImage(img, padding=5, paddingValue=250):

    if img is None:
        return None

    try:
        paddedImage = None
        if len(img.shape) == 2:
            paddedImage = cv2.copyMakeBorder(img, top=padding, bottom=padding, left=padding, right=padding, borderType= cv2.BORDER_CONSTANT, value=[paddingValue])
        elif len(img.shape) == 3:
            paddedImage = cv2.copyMakeBorder(img, top=padding, bottom=padding, left=padding, right=padding, borderType= cv2.BORDER_CONSTANT, value=[paddingValue, paddingValue, paddingValue])

        return paddedImage
    except:
        return None


