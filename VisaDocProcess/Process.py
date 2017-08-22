import cv2
from ImagePreproces import imageBase64 as convrt
from PreProcess import preProcessROICrop, preProcessImageEnhance
from InterfaceManage import getResponseError
from ImplementExtraction import getVisaTextExtraction

def processCamUploadImage(b64_Filedata):

    # Convert base64Image to openCV Image
    openCVImage = convrt.base64_to_openCVImage(b64_Filedata)

    # # Enhance Passport Image improve Ocr Results
    # openCVImage = cv2.cvtColor(openCVImage, cv2.COLOR_BGR2GRAY)

    croppedImage, preProcessAlerts = preProcessROICrop(openCVImage)

    # Run OCR Text Extraction
    # Format extracted data
    if croppedImage is not None:
        croppedImageGray = preProcessImageEnhance(croppedImage)
        extractedData, textExtractionAlerts = getVisaTextExtraction(croppedImageGray)
    else:
        openCVImageGray = preProcessImageEnhance(openCVImage)
        extractedData, textExtractionAlerts = getVisaTextExtraction(openCVImageGray)

    alertMessages = preProcessAlerts + textExtractionAlerts

    if len(alertMessages)>0:
        alertMessages.sort()
        responseError = getResponseError(alertMessages[0])
    else:
        responseError = None

    return extractedData, responseError


def processFileUploadImage(b64_Filedata):

    # Convert base64Image to openCV Image
    openCVImage = convrt.base64_to_openCVImage(b64_Filedata)

    croppedImage, preProcessAlerts = preProcessROICrop(openCVImage)

    # Run OCR Text Extraction
    # Format extracted data
    if croppedImage is not None:
        croppedImageGray = preProcessImageEnhance(croppedImage)
        extractedData, textExtractionAlerts = getVisaTextExtraction(croppedImageGray)
    else:
        openCVImageGray = preProcessImageEnhance(openCVImage)
        extractedData, textExtractionAlerts = getVisaTextExtraction(openCVImageGray)

    alertMessages = preProcessAlerts + textExtractionAlerts

    if len(alertMessages)>0:
        alertMessages.sort()
        responseError = getResponseError(alertMessages[0])
    else:
        responseError = None

    return extractedData, responseError



