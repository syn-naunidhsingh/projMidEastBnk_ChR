

__OUT_RESP_ERR_CODE__ = "code"
__OUT_RESP_ERR_MESG__ = "message"

# Error codes
__ERROR_CODE_DICT__ = {

    0100: "Unable to process the document, please try again",
    1000: "Looks like i can not recognize your Passport. please try again",
    1001: "Sorry your Passport is not clear enough. please try again",
    1004: "Your passport is already expired.",
    1006: "Invalid Date of birth in Passport",
    2000: "Looks like i can not recognize your EID. please try again",
    2001: "Sorry your EID is not clear enough. please try again",
    2004: "Your EID is already expired.",
    2006: "Invalid Date of birth in EID",
    3000: "Looks like I can not recognize your VISA, please try again",
    3001: "Unable to retrieve information from VISA, please provide a clear image",
    3002: "Visa does not contain applicant's passport number.",
    3003: "Visa does not contain applicant's name.",
    3004: "Could not find visa expiry date.",
    3005: "Your visa is already expired.",
    4000: "Could not retrieve salary information",
    4001: "Salary letter cannot be more than 3 month old.",
    4002: "Salary letter cannot be future dated.",
    4003: "Salary letter does not contain applicant's name.",
    4004: "Unable to retrieve salary from the Letter",
    4005: "Unable to run name match in salary letter document analysis, error in parsing input data",
    9001: "Parsing error, unable to parse json input",
    9002: "Unexpected error occured, unable process the document",
}


def getResponseError(err_code):

    responseError = {}
    responseError[__OUT_RESP_ERR_CODE__] = err_code
    try:
        responseError[__OUT_RESP_ERR_MESG__] = __ERROR_CODE_DICT__[err_code]
    except:
        responseError[__OUT_RESP_ERR_MESG__] = "Unknown Error occured"

    return responseError