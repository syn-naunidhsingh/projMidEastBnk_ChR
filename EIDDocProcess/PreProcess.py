import cv2
import numpy as np
import passporteye
from MRZ_Detection import detectMRZ, cropRoiImage

def preprocessCamUpload(cvImage):


    try:

        MRZ_Images = detectMRZ.getMRZ_ROI(cvImage)

        mrz_data = None
        if len(MRZ_Images) > 0:

            for MRZ_Image in MRZ_Images:

                if len(MRZ_Image.shape) > 2:
                    MRZ_Image = cv2.cvtColor(MRZ_Image, cv2.COLOR_BGR2GRAY)

                mrz_data = passporteye.read_mrz(MRZ_Image)

                if mrz_data is None:
                    MRZ_Image = cropRoiImage.rotateImage(MRZ_Image, 180)
                    mrz_data = passporteye.read_mrz(MRZ_Image)

                if mrz_data is not None:
                    break

        if mrz_data is None:
            grayImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
            mrz_data = passporteye.read_mrz(grayImage)

        return mrz_data

    except Exception, e:
        print e
        return None



def preprocessFileUpload(cvImage):


    try:

        MRZ_Images = detectMRZ.getMRZ_ROI(cvImage)

        mrz_data = None
        if len(MRZ_Images) > 0:

            for MRZ_Image in MRZ_Images:

                if len(MRZ_Image.shape) > 2:
                    MRZ_Image = cv2.cvtColor(MRZ_Image, cv2.COLOR_BGR2GRAY)

                mrz_data = passporteye.read_mrz(MRZ_Image)

                if mrz_data is None:
                    MRZ_Image = cropRoiImage.rotateImage(MRZ_Image, 180)
                    mrz_data = passporteye.read_mrz(MRZ_Image)

                if mrz_data is not None:
                    break

        if mrz_data is None:
            grayImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
            mrz_data = passporteye.read_mrz(grayImage)

        return mrz_data

    except Exception, e:
        print e
        return None

#
# img = cv2.imread("/Users/naunidhsingh/Desktop/HSBC/docs/eid/image013.jpg")
# print preprocessCamUpload(img)