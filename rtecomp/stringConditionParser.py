from parse import * # pip install parse

###########################################################################
def removeLeading(key, listToCheck):
    if len(listToCheck) >= 1:
        while (listToCheck[0] == key):
            listToCheck = listToCheck[1:]
            if len(listToCheck) < 1:
                break

    return listToCheck
###########################################################################
def splitOn(keys, listToSplit):
    groupedParts = []
    subGroup = []
    first = True
    for part in listToSplit:
        if first:
            subGroup.append(part)
            first = False
            continue
        found = False
        for key in keys:
            if (part == key):
                found = True
                break
        if found:
            groupedParts.append(subGroup)
            subGroup = []
        else:
            subGroup.append(part)

    if len(subGroup) > 0:
        groupedParts.append(subGroup)

    return groupedParts
###########################################################################
def convertToAlphabet(list, alphabetTemplate):
    alphabet = alphabetTemplate.copy()
    acceptableOthers = ["and"]

    # Weeding out clock conditions
    clockRelated = ["<", "<=", "=", ">=", ">"] # NOTE: Currently, any use of these symbols will cause the ASSUMPTION that it is a clock condition, and it will be ignored
    newListTemp = []
    i = 0
    while i < len(list):
        if (list[i] not in alphabet.keys()) and (list[i] not in acceptableOthers):
            if list[i].startswith("!"):
                # print("Signal not present (! prefix found)")
                if list[i][1:] in alphabet.keys():
                    newListTemp.append(list[i])
                    i += 1
            elif list[i+1] in clockRelated:
                # print("Found clk condition")
                i += 3
            else:
                raise KeyError("An item '" + list[i] + "' in the provided list is not in the alphabet template.")
        else:
            if list[i] not in acceptableOthers:
                newListTemp.append(list[i])
            i += 1

    list = newListTemp

    for i in list:
        if i in acceptableOthers:
            pass # skip?
        # if (i not in alphabet.keys()) and (i not in acceptableOthers):
        #     raise KeyError("An item '" + i + "' in the provided list is not in the alphabet template.")
        if (i.startswith("!")):
            alphabet[i[1:]] = False
        else:
            alphabet[i] = True

    return alphabet
###########################################################################


###########################################################################
# Input:    violatingCondition String, Example: '( X_DOWN and X_UP )'
#           alphabetTemplate, Example: {'X_MIN': None, 'Y_MIN': None, 'X_MAX': None, 'Y_MAX': None, 'X_UP': None, 'X_DOWN': None, 'Y_UP': None, 'Y_DOWN': None, 'RPM_UP': None, 'RPM_DOWN': None}
#
# Processing: 
#
# Output:   violatingCondition (which is an alphabetTemplate which reflects the template)
###########################################################################
def parseConditionString(conditionString, alphabetTemplate):
    # Break on spaces
    parts = []
    part = parse("{} {}", conditionString)
    while part is not None:
        parts.append(part[0])
        part = parse("{} {}", part[1])

    # Break on brackets
    groupedParts = splitOn([")", "("], parts)

    # Break on ORs
    # TODO: Handle leading ANDs
    newGroupedParts = []
    for groupedPart in groupedParts:
        groupedPart = removeLeading("(", groupedPart)
        groupedPart = removeLeading("or", groupedPart)
        if len(groupedPart) > 0:
            newGroupedParts.append(splitOn(["or"], groupedPart))
    groupedParts = newGroupedParts

    i = 0
    while (i < len(groupedParts)):
        current_groupedPart = groupedParts[i]
        # Assumption that each list within groupedParts is an OR, so let's check and fail when that isn't the case
        if (current_groupedPart[0][0] == "and"):
            assert(i > 0) # NOTE: If this fails, somehow your groups start with an "AND"?? Something not right
            previous_groupedPart = groupedParts[i-1]

            # Now, if current_groupedPart is ONLY "and" ([['and']])
            if (len(current_groupedPart[0]) == 1): # NOTE: May not be perfect - what case is [["and", "something"]] vs [["and"], ["something"]]
                # Then we need to add the "and" and the next groupedPart
                assert(i < len(groupedParts))
                next_groupedPart = groupedParts[i+1]
                groupedParts[i-1][-1] = groupedParts[i-1][-1] + current_groupedPart[0] + next_groupedPart[0]
                # groupedParts[i-1][-1].append(next_groupedPart[0])

                # Nullify current and next
                del groupedParts[i]
                del groupedParts[i]

                # and skip one in our loop
                i += 1
            
            # If it is longer than "and" e.g. [["and", "something"]]
            elif (len(current_groupedPart[0]) > 1):  
                # Then we need to add just the current part
                groupedParts[i-1][-1] = groupedParts[i-1][-1] + current_groupedPart[0]
                del groupedParts[i]

        i += 1
      
    newGroupedParts = []
    for groupPart in groupedParts:
        # dictPart = []
        for part in groupPart:
            # dictPart.append(convertToAlphabet(part, alphabetTemplate))
            newGroupedParts.append(convertToAlphabet(part, alphabetTemplate))
        # newGroupedParts.append(dictPart)
    groupedParts =  newGroupedParts
    
    # print(groupedParts)
    return groupedParts
###########################################################################

###########################################################################
def areAnyNone(unwound):
    for anyK in unwound:
        any = unwound[anyK]
        for k in any:
            if any[k] is None:
                return True
    return False
###########################################################################
def getKey(alphabetOption):
    key = ""
    for k in alphabetOption:
        if alphabetOption[k] == True:
            key += "1"
        elif alphabetOption[k] == False:
            key += "0"
        else:
            key += "2"
    return key
###########################################################################
def unwindConditions(conditions):
    # print('Unwinding')
    # print('Unwinding ', conditions)
    unwound = {}
    # print("At start are any more to unwind??", areAnyNone(conditions))
    if not areAnyNone(conditions):
        for conditionKey in conditions:
            unwound[conditionKey] = conditions[conditionKey]
    for conditionKey in conditions:
        condition = conditions[conditionKey]
        for k in condition:
            if condition[k] is None:
                trueOption = condition.copy()
                trueOption[k] = True
                falseOption = condition.copy()
                falseOption[k] = False
                unwound[getKey(trueOption)] = trueOption
                unwound[getKey(falseOption)] = falseOption
    # print("Any more to unwind??", areAnyNone(unwound))
    while areAnyNone(unwound) == True:
        unwound = unwindConditions(unwound)
    # print("Unwound to", unwound)
    return unwound
###########################################################################


###########################################################################
if __name__ == "__main__":
    conditionString = "( !X_UP and !X_DOWN and !Y_UP and !Y_DOWN and V1 <= THRESHOLD and !RPM_UP and !RPM_DOWN )"
    # conditionString = "( ( Y_DOWN and V1 <= THRESHOLD ) or !Y_UP or ( X_UP and X_DOWN ) or RPM_UP or RPM_DOWN )"
    # conditionString = "( Y_UP or X_UP or X_DOWN or RPM_UP or RPM_DOWN )"
    # conditionString = "( ( !X_DOWN and X_UP ) and ( Y_DOWN and !Y_UP ) )"
    alphabet = {'X_MIN': None, 'Y_MIN': None, 'X_MAX': None, 'Y_MAX': None, 'X_UP': None, 'X_DOWN': None, 'Y_UP': None, 'Y_DOWN': None, 'RPM_UP': None, 'RPM_DOWN': None}
    result = parseConditionString(conditionString, alphabet)
    # result = unwindConditions([result])
    print(result)
###########################################################################
