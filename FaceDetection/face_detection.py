
import cv2
import Resources
from pkg_resources import resource_filename

__RESOURCE_PACKAGE_NAME__ = Resources.__name__
facecascade_filename = 'haarcascade_frontalface_default.xml'

faceCascade = cv2.CascadeClassifier(resource_filename(__RESOURCE_PACKAGE_NAME__, facecascade_filename))

def getFaceROI(cvImage):

    # faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    global faceCascade

    img = cvImage[:]
    height, width = img.shape[:2]
    if len(img.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    maxRect = (0,0,0,0)
    for (x, y, w, h) in faces:
        if w*h > maxRect[2]*maxRect[3]:
            maxRect = x, y, w, h



    if maxRect[2]*maxRect[3] > 1:
        x, y, w, h = maxRect
        npRect = np.array([[x,y],[x+w,y],[x,y+h],[x+w,y+h]])
        return npRect

    else:
        return None



