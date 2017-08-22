
import cv2
import passporteye
from MRZ_Detection import detectMRZ
from MRZ_Detection.roi_img_operations import rotateImage

def preprocessCamUpload(cvImage):

    try:

        MRZ_Image = detectMRZ.getMRZ_ROI(cvImage)

        mrz_data = None
        if MRZ_Image is not None:

            if len(MRZ_Image.shape) > 2:
                MRZ_Image = cv2.cvtColor(MRZ_Image, cv2.COLOR_BGR2GRAY)

            mrz_data = passporteye.read_mrz(MRZ_Image)

            if mrz_data is None:
                MRZ_Image = rotateImage(MRZ_Image, 180)
                mrz_data = passporteye.read_mrz(MRZ_Image)


        if mrz_data is None:
            grayImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
            mrz_data = passporteye.read_mrz(grayImage)

        return mrz_data

    except Exception, e:
        print e
        return None



def preprocessFileUpload(cvImage):

    try:

        MRZ_Image = detectMRZ.getMRZ_ROI(cvImage)

        if MRZ_Image is not None:

            if len(MRZ_Image.shape) > 2:
                MRZ_Image = cv2.cvtColor(MRZ_Image, cv2.COLOR_BGR2GRAY)

            mrz_data = passporteye.read_mrz(MRZ_Image)

            if mrz_data is None:
                MRZ_Image = rotateImage(MRZ_Image, 180)
                mrz_data = passporteye.read_mrz(MRZ_Image)

            if mrz_data is None:
                grayImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
                mrz_data = passporteye.read_mrz(grayImage)

            return mrz_data

    except Exception, e:
        print e
        return None

#
# img = cv2.imread("/Users/naunidhsingh/Desktop/HSBC/docs/passport/Fine/ns.jpg")
# print preprocessCamUpload(img)
