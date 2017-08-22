# Passport document process imports
import PassportDocProcess
# EID document process imports
import EIDDocProcess
# Visa document process imports
import VisaDocProcess
# STL document process imports
import STLDocProcess
# Compare Engine import
from CompareEngine import compare_PP2EID, compare_PP2Visa, compare_PP2STL

from Resources import getBase64ResourceImages


def checkStlProcess():

    pass

def checkVisaProcess():

    pass


def checkEidProcess():

    pass


def checkPassportProcess():

    Base64Strings = getBase64ResourceImages()

    currentBase64imgName = "passportSample_Self.txt"

    Base64String = Base64Strings[currentBase64imgName]

    extracted_data, response_error = PassportDocProcess.Process.processCamUploadImage(Base64String)

    print "Extracted Data from Passport :"
    print extracted_data

    print "Error occurred if any :"
    print response_error


if __name__=="__main__":


    checkPassportProcess()

