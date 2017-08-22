import cv2
import imutils
from analyze_contour_detection import getRoiForContours
from roi_img_operations import rotateAndCropMRZ2, padImage
from matrix_operations import resizeMRZRects


__IMAGE_CONST_RESIZE__ = 1000

def detectMRZRoi(image):

    # Reshape image to optimize contour detection
    orig_Height, orig_Width = image.shape[:2]
    image = imutils.resize(image, height=__IMAGE_CONST_RESIZE__)
    chng_Height, chng_Width = image.shape[:2]

    # convert Image to GrayScale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #
    # cv2.imshow("Image", gray)
    # cv2.waitKey(0)

    # Binarize image using adaptive thresholding
    # thresh_init = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] #
    thresh_init = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
    #
    thresh_init = cv2.erode(thresh_init, None, iterations=1)

    # Invert Image
    thresh_init = cv2.bitwise_not(thresh_init)


    # cv2.imshow("Image", thresh_init)
    # cv2.waitKey(0)

    # Loop over to dilate value to find the best match
    for dilateVal in xrange(1,8):

        # Dilate image iteratively to get the MRZ line connected together
        thresh = cv2.dilate(thresh_init, None, iterations=dilateVal)

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

            print "MRZ found"
            return MRZRects


    print "No MRZ Found"
    return []


def combineMRZPair(mrz1, mrz2):

    combMRZ = []
    n_centre = (float(mrz1[0][0] + mrz2[0][0])/2, float(mrz1[0][1] + mrz2[0][1])/2)
    n_angle = float(mrz1[2] + mrz2[2])/2
    w1, h1 = mrz1[1]
    w2, h2 = mrz2[1]
    if w1>h1 and w2>h2:
        n_w = max(w1,w2)
        n_h = 1.55*float(h1+h2)
    elif h1>w1 and h2>w2:
        n_h = max(h1,h2)
        n_w = 1.55*float(w1+w2)

    combMRZ.append(n_centre)
    combMRZ.append((n_w, n_h))
    combMRZ.append(n_angle)

    return tuple(combMRZ)


# Input : OpenCV Image : Raw Coloured image of Passport
# Output : OpenCV Image, OpenCV Image, Validity : Cropped MRZ Section, Cropped Passport ROI, Confirmation document is a passport.
def getMRZ_ROI(cvImage):

    # Get list of minAreaRects containing the pair of ROIs of MRZ Section
    MRZRects = detectMRZRoi(cvImage)

    if len(MRZRects) > 0:
        for pairRect in MRZRects:
            try:
                complete_MRZ_Section = combineMRZPair(pairRect[0], pairRect[1])
                # box = np.int0(cv2.cv.BoxPoints(complete_MRZ_Section))
                # cv2.drawContours(cvImage, [box], -1, (0, 255, 0), 3)
                # cv2.imshow("Image", cvImage)
                # cv2.waitKey(0)
                croppedImage =  rotateAndCropMRZ2(cvImage, complete_MRZ_Section)
                paddedCroppedImage = padImage(croppedImage, 30)
                return paddedCroppedImage

            except:
                print "Unable to extract mrz, raised exception"
                return None

