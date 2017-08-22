
import cv2
import passporteye
import numpy
from ImageConversion import imageBase64 as convrt
from ImplementExtraction import formatPassportEyeData
from InterfaceManage import getResponseError
from PreProcess import preprocessCamUpload, preprocessFileUpload

def processCamUploadImage(b64_Filedata):

    # Convert base64Image to openCV Image
    openCVImage = convrt.base64_to_openCVImage(b64_Filedata)

    # Enhance Passport Image improve Ocr Results
    # openCVImage = cv2.cvtColor(openCVImage, cv2.COLOR_BGR2GRAY)

    # Run passport eye to extract details and
    mrz = preprocessCamUpload(openCVImage)

    # Format extracted data
    extractedData, alertMessages = formatPassportEyeData(mrz)

    if len(alertMessages)>0:
        alertMessages.sort()
        responseError = getResponseError(alertMessages[0])
    else:
        responseError = None

    return extractedData, responseError


def processFileUploadImage(b64_Filedata):

    # Convert base64Image to openCV Image
    openCVImage = convrt.base64_to_openCVImage(b64_Filedata)

    # Enhance Passport Image improve Ocr Results
    openCVImage = cv2.cvtColor(openCVImage, cv2.COLOR_BGR2GRAY)

    # Run passport eye to extract details and
    mrz = preprocessFileUpload(openCVImage)

    # Format extracted data
    extractedData, alertMessages = formatPassportEyeData(mrz)

    if len(alertMessages)>0:
        alertMessages.sort()
        responseError = getResponseError(alertMessages[0])
    else:
        responseError = None

    return extractedData, responseError





