import pytesseract
from PIL import Image

import cv2

from extract_date import getDateFromDocument
from extract_salary import getSalaryFromDocument
from match_name import matchNameFromDocument


def runImageOCR_Ph2(cvImage):

    ret, bin_img = cv2.threshold(cvImage, 127, 255, cv2.THRESH_BINARY)
    pil_img = Image.fromarray(bin_img)
    OCR_result = pytesseract.image_to_string(pil_img, config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/.-, -psm 6")
    return OCR_result

def runImageOCR(cvImage):

    pil_img = Image.fromarray(cvImage)
    OCR_result = pytesseract.image_to_string(pil_img)
    return OCR_result


# Funtion to extract following information:
#       Extract date
#       Verify Name
#       Extract Salary
#       Extract Currency
def extract_info_stl(cvImage, pp_name):


    extracted_result = {}
    alertMesg = []

    try:

        ocrText = runImageOCR(cvImage)

        extracted_date,  date_alert = getDateFromDocument(ocrText)

        extracted_salary, salary_alert = getSalaryFromDocument(ocrText)

        extracted_nameMatch, nameMatch_alert = matchNameFromDocument(ocrText, pp_name)

        extracted_result.update(extracted_date)
        extracted_result.update(extracted_salary)
        extracted_result.update(extracted_nameMatch)

        alertMesg += date_alert + salary_alert + nameMatch_alert

    except:

        alertMesg.append(4000)

    return extracted_result, alertMesg




