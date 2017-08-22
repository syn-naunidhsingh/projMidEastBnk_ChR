from ManageJson import json_names
import datetime

def formatPassportEyeData(mrzData):

    # change format of passport ouput

    extractedData = {}
    alertMessage = []

    try:

        # Get Name and gender
        extractedData[json_names.__PP_NAME__] = mrzData.names + " " + mrzData.surname
        # extractedData[json_names.__PP_GENDER__] = mrzData.sex

        extractedData[json_names.__PP_MRZ_TYPE__] = mrzData.mrz_type
        extractedData[json_names.__PP_COUNTRY__] = mrzData.country

        # Format Passport No:
        extractedData[json_names.__PP_NO__] = str(mrzData.number).replace("<","")

        # Format Date of Expiry:
        if mrzData.expiration_date is not None:
            ValidDate, expiryDate = formatMRZDate(mrzData.expiration_date)
            if ValidDate:
                if expiryDate < datetime.date.today():
                    alertMessage.append(1004) # Code indicating that passport is expired.
                extractedData[json_names.__PP_EXPIRY__] = formatDatetime_Date(expiryDate)
            else:
                extractedData[json_names.__PP_EXPIRY__] = None
        else:
            extractedData[json_names.__PP_EXPIRY__] = None

        # Format Date of Birth
        if mrzData.date_of_birth is not None:
            ValidDate, birthDate = formatMRZDate(mrzData.date_of_birth)
            if ValidDate:
                if birthDate > datetime.date.today():
                    alertMessage.append(1006) # Code indicating that dob is expired.
                extractedData[json_names.__PP_DOB__] = formatDatetime_Date(birthDate)
            else:
                extractedData[json_names.__PP_DOB__] = None
        else:
            extractedData[json_names.__PP_DOB__] = None

        return extractedData, alertMessage

    except Exception, e:
        print e
        print "Unable to format mrz data from passport eye result"
        alertMessage.append(1001) # Code indicating passport details not extracted.
        return extractedData, alertMessage



def formatDatetime_Date(dt):

    return str(dt.day) + " " + __MONTHS__[dt.month] +  " " + str(dt.year)


def ValidateDate(yy, mm, dd):

    try:
        dt = datetime.date(yy, mm, dd)
        Valid = True
    except:
        dt = None
        Valid = False

    return Valid, dt

__MONTHS__ = ('None', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')

def formatMRZDate(mrzString):

    if len(mrzString) == 6:

        try:
            yy = int(mrzString[0:2])
            mm = int(mrzString[2:4])
            dd = int(mrzString[4:6])
            if yy < 41:
                yy = 2000 + yy
            else:
                yy = 1900 + yy

            return ValidateDate(yy, mm, dd)
            # final_Str = str(dd) + " " + __MONTHS__[mm] + " " + str(yy)
            # return final_Str,

        except:
            print "Unable to parse date string from passporteye mrz"
            return False, None


    else:
        print "Invalid String"
        return False, None