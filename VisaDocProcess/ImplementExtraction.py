
import pytesseract
from PIL import Image
from ManageJson import json_names



def getVisaTextExtraction(cvImage_gray):

    extractedData = {}
    alertMessages = []

    try:

        pil_gray_img = Image.fromarray(cvImage_gray)

        visaString = pytesseract.image_to_string(pil_gray_img)

        extractedData[json_names.__VISA_TEXT__] = visaString

    except Exception, e:
        print e

        alertMessages.append(3001) # Code indicating no information extracted from visa

    return extractedData, alertMessages