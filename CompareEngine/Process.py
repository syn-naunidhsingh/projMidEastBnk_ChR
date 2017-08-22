
from match_name import match_name_strings, match_visa_no_strings

from ManageJson import json_names

__EID_COMPARE_THRESHOLD__ = 0.6

__VISA_NAME_COMPARE_THRESHOLD__ = 0.6



def compare_PP2EID(pp_data, eid_data):

    match_dict = {}

    passport_Name = pp_data[json_names.__PP_NAME__]
    eid_Name = eid_data[json_names.__EID_NAME__]

    match_score = match_name_strings(passport_Name, eid_Name)

    if match_score > __EID_COMPARE_THRESHOLD__:
        match_dict[json_names.__MATCH_EID_NAME__] = True
    else:
        match_dict[json_names.__MATCH_EID_NAME__] = False

    return match_dict



def compare_PP2Visa(pp_data, visa_data):

    match_dict = {}

    match_dict[json_names.__MATCH_VISA_NAME__] = False
    match_dict[json_names.__MATCH_VISA_PP_NO__] = False

    passport_Name = pp_data[json_names.__PP_NAME__]
    passport_Num = pp_data[json_names.__PP_NO__]

    Visa_String = visa_data[json_names.__VISA_TEXT__]

    visa_lines = Visa_String.split("\n")


    for line in visa_lines:
        match_score = match_name_strings(passport_Name, line)
        if match_score > __VISA_NAME_COMPARE_THRESHOLD__:
            match_dict[json_names.__MATCH_VISA_NAME__] = True
            break


    for line in visa_lines:
        if match_visa_no_strings(passport_Num, line):
            match_dict[json_names.__MATCH_VISA_PP_NO__] = True
            break

    return match_dict



def compare_PP2STL(STL_data):

    match_dict = {}
    match_dict[json_names.__MATCH_STL_NAME__] = False
    if json_names.__STL_NAME_VALID__ in STL_data:

        if STL_data[json_names.__STL_NAME_VALID__]:
            match_dict[json_names.__MATCH_STL_NAME__] = True
        else:
            match_dict[json_names.__MATCH_STL_NAME__] = False

        del STL_data[json_names.__STL_NAME_VALID__]

    return match_dict





