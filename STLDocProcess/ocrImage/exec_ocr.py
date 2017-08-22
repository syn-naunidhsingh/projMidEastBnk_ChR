import pytesseract
from PIL import Image
import cv2


def runDocImageOCR(cvImage):
    # re_image = cv2.resize(self.gray_image, (0,0), fx=self.resizingFactor[0], fy=self.resizingFactor[1])

    pil_img = Image.fromarray(cvImage)

    OCR_result = pytesseract.image_to_string(pil_img, config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/.-, -psm 6")

    return OCR_result

def runImageOCR(cvImage):
    # re_image = cv2.resize(self.gray_image, (0,0), fx=self.resizingFactor[0], fy=self.resizingFactor[1])

    pil_img = Image.fromarray(cvImage)

    OCR_result = pytesseract.image_to_string(pil_img) #, config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/ -psm 6")

    return OCR_result