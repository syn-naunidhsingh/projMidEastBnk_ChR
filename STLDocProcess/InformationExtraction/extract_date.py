import cv2
from STLDocProcess import ocrImage
import re
import datetime
from InterfaceManage import json_names

__MONTHS__ = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec']

def getConbineList_OR(lst):
    return "|".join(lst)



def match_regex(strng, regx):
    mt = re.search(regx, strng)
    if mt:
        return mt.group()
    else:
        return None


__DATE_REGEX_LIST__ = ["(\d{1,2})[,.-/ ](\d{1,2})[,.-/ ](\d{2,4})",
                       "(\d{1,2})\s?(th|st|rd|nd)?\s?("+getConbineList_OR(__MONTHS__)+")[,]?\s?(\d{2,4})",
                       "("+getConbineList_OR(__MONTHS__)+")[,]?\s?(\d{1,2})\s?(th|st|rd|nd)?[,]?\s?(\d{2,4})"
                       ]

__DATE_GROUP_ORDER__ = [[1,2,3],
                        [1,3,4],
                        [3,1,6]]

# Function to retrieve date of the document.
# Input : String : OCR text output of the document
# Output : Date extracted from the document
def getDateFromDocument(ocrText):

    extracted_date = {}
    alertMesg = []

    lines = ocrText.split("\n")

    for line in lines:
        if len(line) > 6:      # Assuming Date can not be represented in less than 6 characters
            for i in range(len(__DATE_REGEX_LIST__)):
                matched_date = matchDate(line, i)
                if matched_date is not None:
                    alertMesg += checkOldDate(matched_date)
                    extracted_date[json_names.__STL_DATE__] = matched_date
                    return extracted_date, alertMesg


    if len(extracted_date)==0:
        alertMesg.append(4000)

    return extracted_date, alertMesg


def checkOldDate(dt):

    alertMesg = []
    today = datetime.date.today()
    diff = today - dt
    if not diff.days <= 91:
        alertMesg.append(4001)
    elif dt > today:
        alertMesg.append(4002)

    return alertMesg






def matchDate(line, rgexIndex):

    match_found = re.search(__DATE_REGEX_LIST__[rgexIndex], line, re.IGNORECASE)
    try:
        if match_found is not None:
            group_order = __DATE_GROUP_ORDER__[rgexIndex]
            dd = match_found.group(group_order[0])
            mm = match_found.group(group_order[1])
            yy = match_found.group(group_order[2])
            date = formatDate(dd,mm,yy)
            if date is not None:
                return date

        return None
    except:
        print "Unable to match date form line"
        return None




def formatDate(dd,mm,yy):

    try:
        dd = dd.strip()
        mm = mm.strip()
        yy = yy.strip()

        if mm.lower() in __MONTHS__:
            mm = __MONTHS__.index(mm.lower())%12 + 1

        if len(yy) == 2:
            yy = int(yy) + 2000
        else:
            yy = int(yy)

        dd = int(dd)
        mm = int(mm)

        valid, dt = ValidateDate(yy, mm, dd)

        if valid:
            return dt
        else:
            return None
    except:
        print "unable to format date from line match"
        return None



def ValidateDate(yy, mm, dd):

    try:
        dt = datetime.date(yy, mm, dd)
        Valid = True
    except:
        dt = None
        Valid = False

    return Valid, dt


