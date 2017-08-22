
from os import environ
# Flask imports
from flask import Flask, request, jsonify
# json imports
import json
from ManageJson import json_names, getResponseError
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

app = Flask(__name__)




# Function to extract details from the documents:
# Input JSON format :
#           "document_image" : "base_64 Data" - Entire Image encoded in Base 64 format
#           "document_type"  : 1              - Code indicating the type of document input:- { 1: Passport, 2: EID, 3: VISA, 4: STL }
#           "reference_document_data" : { "name" : "value" ...}
#
# Output JSON format :
#           "error"              : { "code" : 1000, "message" : "Document not clear"}
#           "document_data"      : { "name" : "value" ... }
#           "match_verification" : { "field": boolean }
@app.route('/getDocumentDetails', methods=['POST'])
def getDocumentDetails():

    try :

        # Get JSON object from the frontend
        requestJsonObj = json.loads(request.data)

        # Get document type and Image
        document_type = requestJsonObj[json_names.__IN_DOCUMENT_TYPE__]
        document_file = requestJsonObj[json_names.__IN_DOCUMENT_IMAGE__]

        try:
            # Execute OCR engine based on the document type:
            if document_type == json_names.__IN_CODE_PASSPORT_CAM__:
                # Implement OCR on cam uploaded passport document.
                extracted_data, response_error = PassportDocProcess.Process.processCamUploadImage(document_file)
                return frame_output(extracted_data, None, response_error)

            if document_type == json_names.__IN_CODE_PASSPORT_FILE__:
                # Implement OCR on file uploaded passport document.
                extracted_data, response_error = PassportDocProcess.Process.processFileUploadImage(document_file)
                return frame_output(extracted_data, None, response_error)

            if document_type == json_names.__IN_CODE_EID_CAM__:
                # Implement OCR on cam uploaded EID document.
                extracted_data, response_error = EIDDocProcess.Process.processCamUploadImage(document_file)

                reference_document_data = requestJsonObj[json_names.__IN_REF_DOCUMENT_DATA__]
                match_verification = compare_PP2EID(reference_document_data, extracted_data)
                return frame_output(extracted_data, match_verification, response_error)

            if document_type == json_names.__IN_CODE_EID_FILE__:
                # Implement OCR on file uploaded EID document.
                extracted_data, response_error = EIDDocProcess.Process.processFileUploadImage(document_file)

                reference_document_data = requestJsonObj[json_names.__IN_REF_DOCUMENT_DATA__]
                match_verification = compare_PP2Visa(reference_document_data, extracted_data)
                return frame_output(extracted_data, match_verification, response_error)

            if document_type == json_names.__IN_CODE_VISA_CAM__:
                # Implement OCR on cam uploaded Visa document.
                extracted_data, response_error = VisaDocProcess.Process.processCamUploadImage(document_file)
                # print extracted_data, response_error
                reference_document_data = requestJsonObj[json_names.__IN_REF_DOCUMENT_DATA__]
                # print reference_document_data
                match_verification = compare_PP2Visa(reference_document_data, extracted_data)
                return frame_output(extracted_data, match_verification, response_error)


            if document_type == json_names.__IN_CODE_VISA_FILE__:
                # Implement OCR on file uploaded Visa document.
                extracted_data, response_error = VisaDocProcess.Process.processFileUploadImage(document_file)

                reference_document_data = requestJsonObj[json_names.__IN_REF_DOCUMENT_DATA__]
                match_verification = compare_PP2Visa(reference_document_data, extracted_data)
                return frame_output(extracted_data, match_verification, response_error)

            if document_type == json_names.__IN_CODE_STL_CAM__:
                # Implement OCR on cam uploaded Salary Letter document.

                reference_document_data = requestJsonObj[json_names.__IN_REF_DOCUMENT_DATA__]

                extracted_data, response_error = STLDocProcess.Process.processCamUploadImage(document_file, reference_document_data)
                match_verification = compare_PP2STL(extracted_data)
                return frame_output(extracted_data, match_verification, response_error)

            if document_type == json_names.__IN_CODE_STL_FILE__:
                # Implement OCR on file uploaded Salary Letter document.

                reference_document_data = requestJsonObj[json_names.__IN_REF_DOCUMENT_DATA__]

                extracted_data, response_error = STLDocProcess.Process.processCamUploadImage(document_file, reference_document_data)
                match_verification = compare_PP2STL(extracted_data)
                return frame_output(extracted_data, match_verification, response_error)


        except Exception, e:
            print e
            response_error = getResponseError(9002)
            return frame_output({}, None, response_error)


    except Exception, e:
        print e
        response_error = getResponseError(9001)
        return frame_output({}, None, response_error)


def frame_output(extractedData, matchVerification, responseError):

    response_output = {}
    response_output[json_names.__OUT_RESP_DATA__] = extractedData
    response_output[json_names.__OUT_RESP_MATCH_VALID__] = matchVerification
    response_output[json_names.__OUT_RESP_ERR__] = responseError

    return jsonify(response_output)



@app.route('/test', methods=['POST'])
def test():

    jsonObj = json.loads(request.data)
    print jsonObj["data"]

    return "success"


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)

