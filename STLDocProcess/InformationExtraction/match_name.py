import editdistance
from ManageJson import json_names

__SALS__ = ["Mr", "Mrs", "Miss", "Ms", "Dr", "Pr"]

def matchNameFromDocument(ocrText, matchName):

    lines = ocrText.split("\n")

    extracted_name_match = {}
    alertMesg = []
    extracted_name_match[json_names.__STL_NAME_VALID__] = False
    if matchName is None:
        alertMesg.append(4005)

    for line in lines:

        matchFound = matchNameInLine(line, matchName)
        if matchFound:
            extracted_name_match[json_names.__STL_NAME_VALID__] = True
            break

    return extracted_name_match, alertMesg


def matchNameInLine(line, matchName):

    try:
        words = line.split()

        names = matchName.split()

        totalMatch = 0

        for name in names:

            max_match = 0
            match_word = None
            for word in words:

                cur_match = match_name_distance(name, word)

                if cur_match > max_match:
                    max_match = cur_match
                    match_word = word

            totalMatch += max_match
            if max_match > 0:
                words.remove(match_word)


        if totalMatch > 1.4:
            return True
        else:
            return False

    except:
        print "unable to process line while matching name"
        return False






def match_name_distance(Aword, Bword):

    Aword = Aword.replace(".", "")
    Bword = Bword.replace(".", "")

    if len(Aword) == 0 or len(Bword) == 0:
        return 0

    if Aword in __SALS__ or Bword in __SALS__:
        return 0

    if len(Bword) < 3:
        if Aword[0] == Bword[0]:
            return 0.7
        elif Aword[0].lower() == Bword[0].lower():
            return 0.5

    Aword = Aword.lower()
    Bword = Bword.lower()

    diff = editdistance.eval(Aword, Bword)

    baseLength = max(len(Aword), len(Bword))

    matchScore =  1 - (float(diff)/baseLength)

    if matchScore > 0.7:
        return matchScore
    else:
        return 0
