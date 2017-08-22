
# Input format JSON Names:

__IN_DOCUMENT_IMAGE__ = "document_image"
__IN_DOCUMENT_TYPE__ = "document_type"
__IN_REF_DOCUMENT_DATA__ = "reference_document_data"

__IN_CODE_PASSPORT_CAM__  = 101
__IN_CODE_PASSPORT_FILE__ = 102
__IN_CODE_EID_CAM__       = 201
__IN_CODE_EID_FILE__      = 202
__IN_CODE_VISA_CAM__      = 301
__IN_CODE_VISA_FILE__     = 302
__IN_CODE_STL_CAM__       = 401
__IN_CODE_STL_FILE__      = 402


# Output format JSON Names:

__OUT_RESP_DATA__ = "document_details"
__OUT_RESP_MATCH_VALID__ = "match_verification"
__OUT_RESP_ERR__ = "error"




# Passport Collections
__PP_USER_ID__ = "userid"
__PP_NO__ = "passportno"
__PP_NAME__ = "name"
__PP_EXPIRY__ = "expirydate"
__PP_EXPIRY_VD__ = "expiry_valid"
__PP_GENDER__ = "gender"
__PP_DOB__ = "date_of_birth"
__PP_COUNTRY__ = "country"
__PP_MRZ_TYPE__ = "mrz_type"
__PP_ALERT__ = "alert"

# EID Collections
__EID_USER_ID__ = "userid"
__EID_NO__ = "eidno"
__EID_NAME__ = "name"
__EID_EXPIRY__ = "expirydate"
__EID_EXPIRY_VD__ = "expiry_valid"
__EID_GENDER__ = "gender"
__EID_DOB__ = "date_of_birth"
__EID_MRZ_TYPE__ = "mrz_type"
__EID_ALERT__ = "alert"

# VISA Collection
__VISA_NAME__ = "name"
__VISA_NO__ = "visa_no"
__VISA_PP_NO__ = "visa_passport_no"
__VISA_TEXT__ = "visa_text"

# Salary Transfer Letter Collection
__STL_DATE__ = "date"
__STL_NAME_VALID__ = "name_verification"
__STL_SALARY__ = "salary"
__STL_CURRENCY__ = "currency"
__STL_SALARY_PERIOD__ = "period"



# Match Verification
__MATCH_EID_NAME__ = "eid_name_match"

__MATCH_VISA_NAME__ = "visa_name_match"
__MATCH_VISA_PP_NO__ = "visa_passport_no_match"

__MATCH_STL_NAME__ = "stl_name_match"
