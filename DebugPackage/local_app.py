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

import simplejson


def checkStlProcess():

    Base64Strings = getBase64ResourceImages()

    currentBase64imgName = "stlSample_1.txt"

    Base64String = Base64Strings[currentBase64imgName]

    reference_document_data = '''{
        "country": "EGY",
        "date_of_birth": "22 OCT 1988",
        "expirydate": "25 APR 2019",
        "mrz_type": "TD3",
        "name": "MUHAMMAD SAMIR EBRAHIM ALI SHEHATA",
        "passportno": "A06805799"
    }'''

    reference_document_data = simplejson.loads(reference_document_data)

    extracted_data, response_error = STLDocProcess.Process.processCamUploadImage(Base64String, reference_document_data)

    match_verification = compare_PP2STL(extracted_data)

    print "Extracted Data from Passport :"
    print extracted_data

    print "Match Verification"
    print match_verification

    print "Error occurred if any :"
    print response_error

def checkVisaProcess():

    Base64Strings = getBase64ResourceImages()

    currentBase64imgName = "visaSample_1.txt"

    Base64String = Base64Strings[currentBase64imgName]

    extracted_data, response_error = VisaDocProcess.Process.processCamUploadImage(Base64String)

    reference_document_data = '''{
        "country": "EGY",
        "date_of_birth": "22 OCT 1988",
        "expirydate": "25 APR 2019",
        "mrz_type": "TD3",
        "name": "MUHAMMAD SAMIR EBRAHIM ALI SHEHATA",
        "passportno": "A06805799"
    }'''

    reference_document_data = simplejson.loads(reference_document_data)

    match_verification = compare_PP2Visa(reference_document_data, extracted_data)

    print "Extracted Data from Passport :"
    print extracted_data['visa_text']

    print "Match Verification"
    print match_verification

    print "Error occurred if any :"
    print response_error


def checkEidProcess():

    Base64Strings = getBase64ResourceImages()

    currentBase64imgName = "eidSample_Sam.txt"

    Base64String = Base64Strings[currentBase64imgName]

    extracted_data, response_error = EIDDocProcess.Process.processCamUploadImage(Base64String)

    reference_document_data = '''{
        "country": "EGY",
        "date_of_birth": "22 OCT 1988",
        "expirydate": "25 APR 2019",
        "mrz_type": "TD3",
        "name": "MUHAMMAD SAMIR EBRAHIM ALI SHEHATA",
        "passportno": "A06805799"
    }'''

    reference_document_data = simplejson.loads(reference_document_data)

    match_verification = compare_PP2EID(reference_document_data, extracted_data)

    print "Extracted Data from Passport :"
    print extracted_data

    print "Match Verification"
    print match_verification

    print "Error occurred if any :"
    print response_error


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


    # checkPassportProcess()
    checkVisaProcess()


