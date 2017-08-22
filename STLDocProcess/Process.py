import cv2

from ImageConversion import imageBase64 as convrt
from InterfaceManage import getResponseError, json_names
from InformationExtraction import extract_information
# To process passport image uploaded from camera


def processCamUploadImage(b64_Filedata, pp_data):

    # Convert base64Image to openCV Image
    openCVImage = convrt.base64_to_openCVImage(b64_Filedata)

    # Enhance STL Image improve Ocr Results
    openCVImage = cv2.cvtColor(openCVImage, cv2.COLOR_BGR2GRAY)

    # Extract name from the passport
    try:
        matchName = pp_data[json_names.__PP_NAME__]
    except:
        matchName = None


    # Format extracted data
    extractedData, alertMessages = extract_information.extract_info_stl(openCVImage, matchName)

    if len(alertMessages)>0:
        alertMessages.sort()
        responseError = getResponseError(alertMessages[0])
    else:
        responseError = None

    return extractedData, responseError


def processFileUploadImage(b64_Filedata, pp_data):

    # Convert base64Image to openCV Image
    openCVImage = convrt.base64_to_openCVImage(b64_Filedata)

    # Enhance STL Image improve Ocr Results
    openCVImage = cv2.cvtColor(openCVImage, cv2.COLOR_BGR2GRAY)

    # Extract name from the passport
    try:
        matchName = pp_data[json_names.__PP_NAME__]
    except:
        matchName = None

    # Format extracted data
    extractedData, alertMessages = extract_information.extract_info_stl(openCVImage, matchName)

    if len(alertMessages)>0:
        alertMessages.sort()
        responseError = getResponseError(alertMessages[0])
    else:
        responseError = None

    return extractedData, responseError

# img = cv2.imread("/Users/naunidhsingh/Desktop/HSBC/docs/stl/2-1.png")
# grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print extract_information.extract_info_stl(grayImage, "Adele Joyce")[0]
