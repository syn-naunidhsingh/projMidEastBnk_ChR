
from nltk.tokenize import word_tokenize
import editdistance

__SALS__ = ["Mr", "Mrs", "Miss", "Ms", "Dr", "Pr"]

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


def match_name_strings(Aname, Bname):

    # Match two given names, and reference the match score with respect to Aname (Mostly Name Extracted from Passport)

    Aname_words = word_tokenize(Aname)
    Bname_words = word_tokenize(Bname)

    baseLength = len(Aname_words)

    matchScore = 0

    for Aword in Aname_words:

        maxScore = 0
        for Bword in Bname_words:

            currScore = match_name_distance(Aword, Bword)
            if currScore > maxScore:
                maxScore = currScore

        matchScore += maxScore

    matchScore = float(matchScore)/baseLength

    return matchScore


def match_visa_no_strings(Astring, Bstring):

    Btokens = Bstring.split()

    for Btoken in Btokens:

        edist = editdistance.eval(Astring, Btoken)

        edist_score = float(edist)/len(Astring)

        if edist_score < 0.15:

            return True

    return False







