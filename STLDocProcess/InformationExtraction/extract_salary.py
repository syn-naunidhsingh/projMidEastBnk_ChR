import re
from ManageJson import json_names

__SALARY__ = ["salary", "remuneration"]

__SALARY_RGEX__ = [r"(\d+[.,]?)+"]

__SALARY_AUX__ = ["total", "gross", "basic"]

__CURRENCY__ = ["AED", "INR", "USD", "GBP", "JPY", r"\$"]


def match_regex(strng, regx):
    mt = re.search(regx, strng)
    if mt:
        return mt.group()
    else:
        return None


def getSalaryFromDocument(ocrText):

    lines = ocrText.split("\n")

    potential_Salary = []
    alertMesg = []

    for line in lines:
        line = line

        for sal in __SALARY__:


            if sal in line.lower():

                for rgex in __SALARY_RGEX__:

                    if match_regex(line.lower(), rgex) is not None:

                        potential_Salary.append(line)


    potential_Salary = prioritise_potential_sals(potential_Salary)

    salary_extract = getSalaryFromLines(potential_Salary)

    if json_names.__STL_SALARY__ not in salary_extract or salary_extract[json_names.__STL_SALARY__] is None:
        alertMesg.append(4004)

    return salary_extract, alertMesg


def prioritise_potential_sals(potentialSal):

    priority_sals = []

    for aux in __SALARY_AUX__[:2]:
        for sal in potentialSal:
            if aux in sal.lower() and sal not in priority_sals:
                priority_sals.append(sal)

    for aux in __SALARY_AUX__[2:]:
        for sal in potentialSal:
            if aux not in sal.lower() and sal not in priority_sals:
                priority_sals.append(sal)

    for aux in __SALARY_AUX__[2:]:
        for sal in potentialSal:
            if aux not in sal.lower() and sal not in priority_sals:
                priority_sals.append(sal)

    return priority_sals


def getSalaryFromLines(potentialSal):

    salary_extract = {}

    if len(potentialSal) > 0:

        sal_line = potentialSal[0]

        currency = match_regex(sal_line, "("+"|".join(__CURRENCY__)+")")
        salary_extract[json_names.__STL_CURRENCY__] = currency


        salary = None
        for salary_regx in __SALARY_RGEX__:
            salary = match_regex(sal_line, salary_regx)
            if salary is not None:
                break

        salary_extract[json_names.__STL_SALARY__] = salary

        if salary is not None:
            duration_line = sal_line.split(salary)[1]
            duration_words = duration_line.split()
            for word in duration_words:
                if match_regex(word.lower(), "month") or match_regex(word.lower(), "p[.,]m[,.]"):
                    salary_extract[json_names.__STL_SALARY_PERIOD__] = "monthly"
                    break
                elif match_regex(word.lower(), "annual") or match_regex(word.lower(), "annum") or match_regex(word.lower(), "year") or match_regex(word.lower(), "p[.,]a[,.]"):
                    salary_extract[json_names.__STL_SALARY_PERIOD__] = "yearly"
                    break
        else:
            salary_extract[json_names.__STL_SALARY_PERIOD__] = None

    return salary_extract




