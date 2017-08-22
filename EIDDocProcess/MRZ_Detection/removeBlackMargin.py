
import numpy as np
import cv2

def autocrop(image, threshold=0, invert=False, padding=0):
    """Crops any edges below or equal to threshold

    Crops blank image to 1x1.

    Returns cropped image.

    """
    if len(image.shape) == 3:
        flatImage = np.max(image, 2)
    else:
        flatImage = image
    assert len(flatImage.shape) == 2
    w,h = flatImage.shape
    if invert:
        flatImage = cv2.bitwise_not(flatImage)

    rows = np.where(np.max(flatImage, 0) > threshold)[0]
    if rows.size:
        cols = np.where(np.max(flatImage, 1) > threshold)[0]
        x1 = max(cols[0]-padding, 0)
        x2 = min(cols[-1] + 1 + padding, w)
        y1 = max(rows[0]-padding, 0)
        y2 = min(rows[-1] + 1 + padding, h)
        image = image[x1: x2, y1: y2]
    else:
        image = image[:1, :1]

    return image


#
# path = "/Users/naunidhsingh/Desktop/HSBC/docs/eid"
#
# a = cv2.imread(path + "/8.png")
#
# b = autocrop(a, 80, True, 90)
#
# cv2.imshow("img", b)
#
# cv2.waitKey()