


# Constants Strings used

__SUCCESS__ = "success"
__FAILURE__ = "failure"

__MESSAGE__ = "message"
__ALERT__ = "alert"

__STATUS__ = "status"
__DATA__ = "data"
__CODE__ = "code"

__ERROR__ = "error"

__UUID__ = "unique_id"


__DOC_IMAGE__ = "document_image"
__DOC_DATA__ = "document_data"

__PP_DOC_DATA__ = "passport_document_data"


ERROR_CODE_DICT = {
    1000: "Looks like i can not recognize your Passport. please try again",
    1001: "Sorry your Passport is not clear enough. please try again",
    1004: "Your passport is already expired.",
    1006: "Invalid Date of birth in Passport",
    2000: "Looks like i can not recognize your EID. please try again",
    2001: "Sorry your EID is not clear enough. please try again",
    2004: "Your EID is already expired.",
    2006: "Invalid Date of birth in EID",
    3000: "Could not retrieve visa information",
    3001: "Visa does not contain applicant's passport number.",
    3002: "Visa does not contain applicant's name.",
    3003: "Could not find visa expiry date.",
    3004: "Your visa is already expired.",
    4000: "Could not retrieve salary information",
    4001: "Salary letter cannot be more than 3 month old.",
    4002: "Salary letter cannot be future dated.",
    4003: "Salary letter does not contain applicant's name.",
}



# functions to frame return message
def dbSubmission(status, mesg = "", data = None, alert = None):

    retMesg = {}
    if status:
        retMesg[__STATUS__] = __SUCCESS__
    else:
        retMesg[__STATUS__] = __FAILURE__
    retMesg[__MESSAGE__] = mesg
    retMesg[__DATA__] = data
    return retMesg


def alertFrame(alertCode):
    alertDict = {}
    alertDict[__CODE__] = alertCode
    if alertCode in ERROR_CODE_DICT:
        alertDict[__MESSAGE__] = ERROR_CODE_DICT[alertCode]
    else:
        alertDict[__MESSAGE__] = None
    return alertDict


def returnFrame(status, uniqueId, data = None, alert = None):

    retMesg = {}
    if status:
        retMesg[__STATUS__] = __SUCCESS__
    else:
        retMesg[__STATUS__] = __FAILURE__

    if data is not None and __ALERT__ in data:
        retMesg[__ERROR__] = alertFrame(data[__ALERT__])
        del data[__ALERT__]
    else:
        retMesg[__ERROR__] = None

    retMesg[__DATA__] = data

    retMesg[__UUID__] = uniqueId

    return retMesg




