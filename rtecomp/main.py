
from parse import * # pip install parse
import pprint
import xml.etree.ElementTree as ET
import sys

###########################################################################
# Helper Functions

def convertInterfaceToBoolDict(root):
    alphabet = {}
    keyLength = 0 # This will determine the length of the key that we will use to capture the dictionary
    for alphabetItem in root.iter("Interface"):
        for child in alphabetItem:
            if child.get("Type") != "bool":
                print("Support for boolean interfaces only!")
                assert(child.get("Type") == "bool")
            if child.get("Constant") == "false":
                print("Added ", child.get("Name"))
                keyLength += 1
                alphabet[child.get("Name")] = None

    return alphabet, keyLength

def parse_validateNoBrackets(conditionStr):
    if conditionStr.__contains__("(") or conditionStr.__contains__(")"):
        print("Condition string provided has brackets CHECK!")
        return False
    else:
        return True

def parse_isOR(conditionStr):
    assert(parse_validateNoBrackets(conditionStr))
    if parse("{}or{}", conditionStr) is None:
        return False
    else:
        return True

def parse_isAND(conditionStr):
    assert(parse_validateNoBrackets(conditionStr))
    if parse("{}and{}", conditionStr) is None:
        return False
    else:
        return True

def areAnyNone(unwound):
    for anyK in unwound:
        any = unwound[anyK]
        for k in any:
            if any[k] is None:
                return True
    return False

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
    
def pad(number, width):
    b = '{0:b}'.format(number)
    # Pad with 0s as required to meet length
    toPad = width - len(b)
    b = "0" * toPad + b
    return b

def getAllConditions(alphabet):
    # Get list of boolean combinations
    keys = alphabet.keys()
    width = len(keys)

    highest = pow(2, width)

    conditions = []

    for i in range(0, highest):
        conditions.append(pad(i, width))

    # Take each bool combo and turn into dict
    newConditions = {}
    for condition in conditions:
        newCondition = {}
        i = 0
        for key in keys:
            newCondition[key] = condition[i]
            i += 1
        newConditions[condition] = newCondition

    return newConditions

def addIfNotPresent(existing, new):
    notPresent = []
    for n in new:
        for e in existing:
            if n == e:
                break
        notPresent.append(n)
    existing = existing + notPresent
    return existing

def parse_singleSignal(signalString):
    if signalString[0] == "!":
        return {"signal":str(signalString[1:]).upper(),"value": False}
    else:
        return {"signal":str(signalString).upper(),"value": True}

def isClockCondition(conditionString):
    # In non-valued enforcement, we can assume any condition like <= < > >=
    if ("<" in conditionString) or ("<=" in conditionString) or (">" in conditionString) or (">=" in conditionString):
        return True
    else:
        return False

def isSingleSignal(conditionString, alphabetTemplate):
    if conditionString[0] == "!":
        conditionString = conditionString[1:]

    for option in alphabetTemplate:
        print(conditionString, option, alphabetTemplate[option])
        if conditionString == option:
            return True
    return False

def getCharacterRepeated(count, char):
    repeated = ""
    for number in range(0, count) : repeated = repeated + str(char)
    return repeated

def getIntersection(first, second):
    intersection = {}
    for f in first:
        # if f in second:
        for s in second:
            if f == s:
                # print("Found a match")
                intersection[f] = second[f]
        # else:
            # print("Found NO match", first[f])
    # print("First: ", first)
    # print("Second: ", second)
    # print("Intersection: ", intersection)
    return intersection

def removeClockConditions(conditions, alphabetTemplate):
    withoutClockConditions = {}
    for condition in conditions:
        # print(condition,conditions[condition])
        conditionValue = {}
        for value in conditions[condition]:
            if value in alphabetTemplate:
                conditionValue[value] = conditions[condition][value]
        # print(condition[0:len(alphabetTemplate)], conditionValue)
        withoutClockConditions[condition[0:len(alphabetTemplate)]] = conditionValue
    return withoutClockConditions

def removeClockConditionKeys(conditions, alphabetTemplate):
    assert(False)
    withoutClockConditions = {}
    for condition in conditions:
        # print('hi2', condition, conditions)#[condition], len(alphabetTemplate))
        # conditionValue = {}
        # for value in conditions[condition]:
        #     if value in alphabetTemplate:
        #         conditionValue[value] = conditions[condition][value]
        # print(condition[0:len(alphabetTemplate)], conditionValue)
        withoutClockConditions[condition[0:len(alphabetTemplate)]] = conditions[condition]
    return withoutClockConditions

def stripClockConditionsFromKey(key, alphabetKeyLength):
    # print("alphabetKeyLength:", alphabetKeyLength, "long, Key is", len(key), "long")
    return key[0:alphabetKeyLength]

def convertKeyToBools(key, alphabetTemplate, allowNone=False):
    dictCondition = {}
    alphabet = list(alphabetTemplate.keys())
    for i in range(0, len(alphabet)):
        if key[i] == "1":
            dictCondition[alphabet[i]] = True
        elif key[i] == "0":
            dictCondition[alphabet[i]] = False
        else:
            if allowNone:
                dictCondition[alphabet[i]] = None
            else:
                assert(False)
    return dictCondition

def convertConditionListToDictOfBools(listOfConditions, alphabetTemplate):
    dictOfConditionSets = {}
    for conditionSet in listOfConditions:
        label = ""
        for key in alphabetTemplate.keys():
            if conditionSet[key] == True:
                label += "1"
            elif conditionSet[key] == False:
                label += "0"
            elif conditionSet[key] is None:
                label += "2"
            else:
                assert(False)

        dictOfConditionSets[label] = conditionSet

    # dictOfConditionSets = unwindConditions(dictOfConditionSets)

    return [dictOfConditionSets, None]

    # print(alphabetTemplate)
    print(conditionString)

    # Remove spaces
    a = conditionString.replace(" ", "")
    # print("Original", a)
    
    # Count number of brackets
    left = a.count("(")
    right = a.count(")")
    assert(left == right)

    # If even count of brackets, there is a missing set of brackets on outer most (true always?)
    if (left % 2 == 0):
        # print("Even;", left)
        count = 1
    else:
        # print("Odd;", left)
        count = 0

    # Remove topmost brackets
    b = parse("({})", a)
    if b is not None:
        while True:
            # Keep going till all top brackets gone
            if parse("({})", b[0]) is not None:
                # print("Part:", b[0])
                b = parse("({})", b[0])
                count += 1
            else:
                break
    
        # print("Top brackets removed:", count, b[0])
    else: 
        b=[]
        # print("No brackets to remove..?", a)
        b.append(a)

    if count > 0:
        # Separate into LHS, condition and RHS
        # Example: !AandB)or(AandB 
        # Becomes: <Result ('!AandB', 'or', 'AandB') {}>
        formatString = "{}" + getCharacterRepeated(count, ")") + "{}" + getCharacterRepeated(count, "(") + "{}"
        # print(formatString)
        topCondition = parse(formatString, b[0])

        # print(topCondition)
        # assert (topCondition is not None)
        if (topCondition is None):
            print("You need to do something Mr Alex")

        
        # TODO: Recursively find all transitions - keep going till you have ONLY ANDS in a list/table

        LHS = topCondition[0]
        RHS = topCondition[2]

        # print("LHS:", LHS, "RHS:", RHS)
        # L = parse_noBracketsCondition(LHS, alphabetTemplate)
        L, clkL = convertConditionToDictOfBools("("+LHS+")", alphabetTemplate)
        # R = parse_noBracketsCondition(RHS, alphabetTemplate)
        R, clkR = convertConditionToDictOfBools("("+RHS+")", alphabetTemplate)

        # Condition is either "AND" or "OR"
        # print("top condition: ", topCondition)

        # Check if either is clock condition
        if isClockCondition(topCondition[0]):
            # print(topCondition[0], "is clock condition")
            topCondition = {**R}
            clk = {**L}
        elif isClockCondition(topCondition[2]):
            # print(topCondition[2], "is clock condition")
            topCondition = {**L}
            clk = {**R}
        else:
            # Neither is sole clock condition, so check how we need to combine
            condition = topCondition[1].lower()
            if (condition == "or"):
                # OR means APPEND sets of conditions for transition to violation
                print("OR")
                topCondition = {**L, **R}
            elif (condition == "and"):
                # AND means INTERSECTION of sets of conditions for transition to violation
                print("AND")
                topCondition = getIntersection(L, R)
        
            clk = {}
    else:
        print(b, b[0])
        topCondition, clk = parse_noBracketsCondition(b[0], alphabetTemplate)

    # print("Returning: ", topCondition, "and clk", clk)
    return topCondition, clk

def convertConditionToDictOfBools(conditionString, alphabetTemplate):
    import stringConditionParser

    listOfConditions = stringConditionParser.parseConditionString(conditionString, alphabetTemplate)

    return convertConditionListToDictOfBools(listOfConditions, alphabetTemplate)

def getAcceptableTransitions(violationConditions, allConditions):
    violationConditionsNoClocks = violationConditions #removeClockConditionKeys(violationConditions, alphabetTemplate)
    # print("with clocks:", violationConditions)
    # print("without clocks:", violationConditionsNoClocks)
    acceptableTransitions = {}
    allConditions = allConditions.copy()
    for condition in allConditions: # TODO: Come up with a way to compare while ignoring any clock conditions?
        if condition in violationConditionsNoClocks:
            pass
        else:
            acceptableTransitions[condition] = allConditions[condition]

    # print("Acceptable Transitions (", len(acceptableTransitions), ") -", acceptableTransitions)
    print("Acceptable Transitions (", len(acceptableTransitions), ")")
    print("Violating Transitions (", len(violationConditions), ")")
    print("All Conditions (", len(allConditions), ")")
    # print("Violating Transitions (", len(violationConditions), ") -", violationConditions)
    assert(len(acceptableTransitions) + len(violationConditions) == len(allConditions))
    return acceptableTransitions

# Provided two binary numbers (as STRINGS)
# This function will calculate the number of bits difference between the two
def calculateDistanceBetween(condition1, condition2):
    assert(len(condition1) == len(condition2))
    # assert(type(condition1) == type.String)
    distance = 0
    for i in range(0, len(condition1)):
        # print(i, condition1[i], condition2[i], condition1[i] == condition2[i])
        if (condition1[i] != condition2[i]):
            distance += 1
    return (distance)

def convertBinaryStringToTextCondition(binaryString, alphabetTemplate):
    # print(binaryString)
    i = 0
    condition = []
    for k in alphabetTemplate:
        if int(binaryString[i]) == 1:
            condition.append(k)
        else:
            condition.append("!"+k)

        # print(k, binaryString[i], condition)
        i += 1

    textCondition = "(" + condition[0]
    i = 0
    for i in range(1, len(condition)):
        textCondition += " and " + condition[i]
    textCondition += ")"

    return textCondition

def convertBinaryRecoveryStringToTextListRecovery(recoveryString, alphabetTemplate):
    recoveryList = []

    i = 0
    for a in alphabetTemplate:
        recoveryList.append({
            "VarName": a,
            "Value": recoveryString[i]
        })
        i += 1

    return recoveryList

def writeNewXML_two(root, input_filename, output_filename, policies, alphabetTemplate, list_intersections, references, individualRecoveryKeys):
    print("======================================")
    print(" WRITING XML FILE")
    print("======================================")
    from bs4 import BeautifulSoup

    # Reading data from the xml file
    with open(input_filename, 'r') as f:
        data = f.read()

    # Passing the data of the xml
    # file to the xml parser of
    # beautifulsoup
    bs_data = BeautifulSoup(data, features='xml')

    for policyTag in bs_data.find_all("Policy"):
        policy = policyTag.attrs["Name"]
        # location = tag.find("Source").text
        for tag in policyTag.find_all("PTransition"):
            location = tag.find("Source").text

            # Change the value of RecoveryReference to match the references list
            recoveries = tag.find_all("RecoveryReference")
            for recovery in recoveries:
                recovery.string = str(references[policy][location])
                # NOTE: Could add something here to add in individualRecoveryKeys[policy][location] to the xml for easier compiling 

    # TODO: LUT with policies variable
    topEnfFnTag = bs_data.find("EnforcedFunction")
    selectLUTTag = bs_data.new_tag("SelectLUT")
    for row in list_intersections:
        rowTag = bs_data.new_tag("Row")

        recoveryTag = bs_data.new_tag("Recovery")
        recoveryTag.append(row["randEdit"]["key"])
        recoveryKeyTag = bs_data.new_tag("RecoveryKey")
        # recoveryKeyTag.append(row["recoveryKey"])
        recoveryKeyTag.append(row["recoveryKey"])

        for policy in policies:
            pRefTag = bs_data.new_tag("PolicyRef", Policy=str(policy), RecoveryReference=str(references[policy][row[policy]]), RecoveryReferenceKey=str(individualRecoveryKeys[policy][row[policy]]))
            rowTag.append(pRefTag)

        for signal in row["randEdit"]["signals"].keys():
            sigName = str(signal)
            sigValue = str(row["randEdit"]["signals"][sigName])

            if sigValue != "None":
                pRecoverTag = bs_data.new_tag("Recover")
                pSig = bs_data.new_tag("Signal")
                pSig.append(sigName)
                pVal = bs_data.new_tag("Value")
                pVal.append(sigValue)
                pRecoverTag.append(pSig)
                pRecoverTag.append(pVal)
                rowTag.append(pRecoverTag)

        rowTag.append(recoveryTag)
        rowTag.append(recoveryKeyTag)
        selectLUTTag.append(rowTag)

    topEnfFnTag.append(selectLUTTag)

    # Output the contents of the
    # modified xml file
    with open(output_filename, "w") as f2:
        # f2.write(str(bs_data.prettify()))
        f2.write(str(bs_data))
        f2.close()
        
###########################################################################

def main(dir, file):
    print("======================================")
    print(" READING & PARSING EXISTING XML FILE")
    print("======================================")

    # Passing the path of the
    # xml document to enable the
    # parsing process
    input_filename = "example/"+dir+"/"+file+".xml"
    output_filename = "example/"+dir+"/"+file+"_modified.xml"
    # tree = ET.parse('example/abc5/abc5.xml')
    tree = ET.parse(input_filename)
    
    # getting the parent tag of
    # the xml document
    originalXMLRoot = tree.getroot()
    
    # printing the root (parent) tag
    # of the xml document, along with
    # its memory location
    print("Enforced Function: ", originalXMLRoot.attrib.get("Name"))

    alphabetTemplate, alphabetKeyLength = convertInterfaceToBoolDict(originalXMLRoot)

    # root.tag
    # root.attrib
    # for child in root:
    #     print(child.tag, child.attrib)
    #     for childchild in child:
    #         print("\t", childchild.tag, childchild.attrib)

    print("==========================================")
    print(" DETERMINE ALL POSSIBLE CONDITIONS")
    print("==========================================")
    print(" - This may take a moment")
    allConditions = getAllConditions(alphabetTemplate.copy())
    print(" - Unique combinations of I/O: ", len(allConditions))

    print("==========================================")
    print(" COLLECTING ALL VIOLATING TRANSITIONS")
    print("==========================================")

    # Find each policies violating transitions
    policies = {}
    table_acceptingTransitions = {}
    table_violatingTransitions = {}
    for policy in originalXMLRoot.iter("Policy"):

        allViolationTransitions = []
        policyViolationCount = 0
        locations = []
        for transition in policy.iter('PTransition'):
            # if (transition.find('Recover')):
            if (transition.find('Destination').text == "violation"):
                # Recovery Statement / PTransition -> Violating

                violatingConditionString = transition.find("Condition").text
                violatingCondition, _ = convertConditionToDictOfBools(violatingConditionString, alphabetTemplate)

                pName = policy.attrib.get("Name")
                location = transition.find("Source").text
                condition = {
                    "string": violatingConditionString,
                    "bool": violatingCondition
                }

                if pName not in table_violatingTransitions.keys():
                    table_violatingTransitions[pName] = {}

                if location not in table_violatingTransitions[pName]:
                    table_violatingTransitions[pName][location] = []

                table_violatingTransitions[pName][location].append(condition)

                break

                # print(policy.attrib.get("Name"), " ", transition.find("Source").text, " to ", transition.find("Destination").text, " on ", transition.find("Condition").text, ". Recovers with ", child.find("VarName").text, child.find("Value").text)
                violationConditions, _ = convertConditionToDictOfBools(transition.find("Condition").text, alphabetTemplate)
                # print(policy.attrib.get("Name"), " ", transition.find("Source").text, " to ", transition.find("Destination").text, " on ", transition.find("Condition").text, ". Recovers with ", child.find("VarName").text, child.find("Value").text)
                # print("Violation Conditions: ", violationConditions)
                acceptable = getAcceptableTransitions(violationConditions, allConditions)
                location = transition.find("Source").text

                for violatingCondition in violationConditions:
                    # Put each violating signal set into table, [policy, reference, location, A, B, C, acceptable resolutions] 
                    policyViolationCount += 1 # TODO: Review renaming this, not always a violating trans
                    allViolationTransitions.append({
                        "policy":policy.attrib.get("Name"),
                        "violationRef":policyViolationCount,
                        "location":location,
                        "violatingConditionString":transition.find("Condition").text,
                        "violatingCondition":stripClockConditionsFromKey(violatingCondition, alphabetKeyLength),
                        "acceptableConditions":acceptable
                    })

                if location not in locations:
                    locations.append(location)
                    policyViolationCount += 1 # TODO: Review renaming this
                    allViolationTransitions.append({
                        "policy":policy.attrib.get("Name"),
                        "violationRef":policyViolationCount,
                        "location":location,
                        "violatingConditionString":"NONE",
                        "violatingCondition":"NONE",
                        "acceptableConditions":acceptable
                    })
            else:
                # Normal Transition Statement / PTransition -> Accepting
                acceptConditionString = transition.find("Condition").text
                acceptCondition, _ = convertConditionToDictOfBools(acceptConditionString, alphabetTemplate)

                pName = policy.attrib.get("Name")
                location = transition.find("Source").text
                condition = {
                    "string": acceptConditionString,
                    "bool": acceptCondition
                }

                if pName not in table_acceptingTransitions.keys():
                    table_acceptingTransitions[pName] = {}

                if location not in table_acceptingTransitions[pName]:
                    table_acceptingTransitions[pName][location] = []

                table_acceptingTransitions[pName][location].append(condition)

        policies[policy.attrib.get("Name")] = allViolationTransitions

    # Add non-violation for each location in each policy 
    # (because there is still some set of acceptable I/O for each policy+location, 
    # and we need to capture this to ensure edit action doesnt inadvertantly violate)
    def getUniqueLocations(policy):
        locations = []
        for violation in policy:
            if violation["location"] not in locations:
                locations.append(violation["location"])
        return locations

    def addRecovery(recoveries, transitionInfo, recovery):
        recoveries[transitionInfo["policy"]+"-"+transitionInfo["location"]+"-"+transitionInfo["violatingCondition"]] = {
            "policy":transitionInfo["policy"],
            "location":transitionInfo["location"],
            "violationRef":transitionInfo["violationRef"],
            "violatingConditionString":transitionInfo["violatingConditionString"],
            "violatingCondition":transitionInfo["violatingCondition"],
            "recovery":recovery
        }
        return

    print("==========================================")
    print(" CREATING VIOLATION REF TABLE")
    print("==========================================")

    def getNumberLocations(policy):
        return len(getUniqueLocations(policy))

    # Create template to be used as rows (each policy should have a column, which will hold the violation reference)
    rowTemplate = {}
    for policy in policies:
        rowTemplate[policy] = 1 

    numberRowsExpected = 1
    # recoveryKeyLength = {} NOTE: Determined later 
    for policy in policies:
        # numberLocations = getNumberLocations(policies[policy])
        numberRowsExpected = numberRowsExpected * (len(policies[policy])) 
        # recoveryKeyLength[policy] = len('{0:b}'.format(len(policies[policy])))  NOTE: Determined later 

    print("Expected Recovery Rows:", numberRowsExpected)

    rowsExample = []
    rowsExample.append(rowTemplate)
    for policy in policies:
        rowCount = len(rowsExample)
        for i in range(rowCount):
            for violation in policies[policy]:
                if violation["violationRef"] > 1: # Added check here to remove don't cares
                    row = rowsExample[i].copy()
                    row[policy] = violation["violationRef"]
                    rowsExample.append(row)

    # assert(len(rowsExample) == numberRowsExpected)

    # List of dictionaries with each policy and violation refs
    import pprint
    # pprint.pprint(rowsExample)

    print("=============================================")
    print(" PRE-CRUNCHING EDITS FOR VIOLATION REF COMBO")
    print("=============================================")

    def convertTableRow_policy_location_to_boolCondition(row_policy_location_condition):
        condition = {}
        for cdtn in row_policy_location_condition:
            condition.update(cdtn["bool"])
        return condition

    def appendViolatingTransitionsToList(combinations, violatingPolicyLocations):
        newCombinations = []
        for combination in combinations:
            newCombinations.append(combination)
        return newCombinations

    def appendPolicyLocationsToList(combinations, policyLocations):
        newCombinations = []
        for combination in combinations:
            policy = policyLocations[0]
            locations = policyLocations[1]
            if policy not in combination.keys():
                for location in locations:
                    combination[policy] = location
                    newCombinations.append(combination.copy())
            else:
                newCombinations.append(combination)

        return newCombinations

    # Make a nice list of policies, with a list inside of each location
    # policies_and_locations = [ [ policy 1 name, [policy location 1, policy location 2, .. ]] ]
    print(" - Getting acceptable actions")
    policies_and_locations = []
    policies = list(table_acceptingTransitions.keys())
    for policy in policies:
        locations = list(table_acceptingTransitions[policy].keys())
        policies_and_locations.append([policy, locations])

    # TODO: Add non-violating for each 

    # Now, for some fun..
    # So we need precompute the intersection of acceptable actions for each location within each policy
    #
    # What? 
    #
    # At any time, each policy is in any one location, and there is a set of acceptable actions in that policy
    # At the same time, EVERY other policy is in any one location, also with a set of acceptable actions
    #
    # In order to precompute edits, we need to determine the intersection of each possible set of locations
    # [Policy1 Locations] X [Policy 2 Locations] X [Policy 3 Locations] and so on
    #
    # Yes it is exponential. So maybe we won't precompute the intersection, but knowing the list of these combinations will be handy.. I think!
    combinations = []
    firstPolicy = policies_and_locations[0]
    for location in firstPolicy[1]:
        combinations.append({firstPolicy[0]: location})
    for policy in policies_and_locations:
        combinations = appendPolicyLocationsToList(combinations, policy)

    def unionDictTransitions(list):
        start = {}
        for i in list:
            start = {**start, **i["bool"]}
        return start

    def intersectionDictTransitions(one, two, alphabetTemplate):
        oneKeys = []
        for item in one:
            # oneKeys.append(list(item["bool"].keys())[0])
            # oneKeys.append(item["bool"].keys())
            oneKeys = oneKeys + list(item["bool"].keys())
        twoKeys = []
        for item in two:
            twoKeys = twoKeys + list(item["bool"].keys())
            # twoKeys.append(list(item["bool"].keys())[0])

        intersection = []
        # for each key in one
        # for oneKey in oneKeys:
        #     # if key is in two
        #     if oneKey in twoKeys:
        #         # add to intersection
        #         intersection[oneKey] = convertKeyToBools(oneKey, alphabetTemplate, allowNone=True) #one[oneKey]

        # If intersection is none, then we need to be more thoughtful
        # intersectionFound = False
        # Specifically comparing for 2s, which are nones- and therefore we dont mind what they are
        for oneKey in oneKeys:
            for twoKey in twoKeys:
                match = True
                for i in range(0, len(oneKey)):
                    # If 0 in onekey, then accept 0 / 2 in twokey
                    if (oneKey[i] == "0"):
                        if (twoKey[i] != "0") and (twoKey[i] != "2"):
                            # Key doesn't match
                            match = False
                            break
                    # If 1 in onekey, then accept 1 / 2 in twokey
                    elif (oneKey[i] == "1"):
                        if (twoKey[i] != "1") and (twoKey[i] != "2"):
                            # Key doesn't match
                            match = False
                            break

                    # If 2 in onekey, then accept any in twokey
                    elif (oneKey[i] == "2"):
                        continue
                    
                if match:
                    jointKey = ""
                    for i in range(0, len(oneKey)):
                        if (oneKey[i] == "2"):
                            jointKey += twoKey[i]
                        elif (twoKey[i] == "2"):
                            jointKey += oneKey[i]
                        else:
                            jointKey += oneKey[i]
                    intersection.append(
                        {"bool":
                         {jointKey: convertKeyToBools(jointKey, alphabetTemplate, allowNone=True)}
                         })
                    # print("Match", oneKey, twoKey, jointKey)
                # else:
                    # print("No-Match", oneKey, twoKey)
                    

                # for oAK in oneAgnosticKey:
                #     if oAK in twoAgnosticKey:
                #         intersection[oAK] = convertKeyToBools(oAK, alphabetTemplate)
                        # intersectionFound = True
                        # break

        return intersection

    print(" - Getting intersection of acceptable actions")
    # For every combination of locations
    list_intersections = []
    # for combination in combinations:
    #     policies = list(combination.keys())
    #     firstPolicy = policies[0]
    #     firstLocation = combination[firstPolicy]
    #     # Union of acceptable for the first policy
    #     acceptableTransitions = unionDictTransitions(table_acceptingTransitions[firstPolicy][firstLocation])
        
    #     # Then for each other policy
    #     for next in policies:
    #         # nextPolicy = next[0]
    #         nextPolicy = next
    #         nextLocation = combination[nextPolicy]
    #         if nextPolicy != firstPolicy:
    #             # Get union of acceptable
    #             someNewAcceptableTransitions = unionDictTransitions(table_acceptingTransitions[nextPolicy][nextLocation])
    #             # Get intersection
    #             acceptableTransitions = intersectionDictTransitions(acceptableTransitions, someNewAcceptableTransitions, alphabetTemplate)

    #     import random
    #     numAccTrans = len(acceptableTransitions)
    #     assert(numAccTrans > 0)
    #     if numAccTrans > 1:
    #         randInt = random.randrange(len(acceptableTransitions)-1)
    #     else:
    #         randInt = 0

    #     randKey = list(acceptableTransitions.keys())[randInt]
    #     # Now we have the intersection, add it to the list
    #     list_intersections.append({
    #         **combination, 
    #         "intersection":acceptableTransitions,
    #         "randEdit":{"key":randKey, "signals":acceptableTransitions[randKey]}
    #     })

    print(" - For each violation")
    for combination in combinations:
        # Combination holds a location for each policy
        # In this combination we can have one or more violating transitions
        # TODO: We need to solve each one of these
        first = True
        accepting = {}
        for policy in policies:
            location = combination[policy]
            # print(policy, location, "violating transitions:", len(table_violatingTransitions[policy][location]), "condition[0]", table_violatingTransitions[policy][location][0]["string"])
            # print("accepting:", table_acceptingTransitions[policy][location][0]['bool'])
            if first:
                accepting = table_acceptingTransitions[policy][location]
                first = False
            else:
                accepting = intersectionDictTransitions(accepting, table_acceptingTransitions[policy][location], alphabetTemplate)
        # print(" - Combination ", combination, "has resolutions:")
        # pprint.pprint(accepting)

        import random
        numAccTrans = len(accepting)
        assert(numAccTrans > 0)
        if numAccTrans > 1:
            randInt = random.randrange(0, len(accepting)) # may need len -1
        else:
            randInt = 0

        print("\t - Found " + str(numAccTrans) + " accepting solutions. Picked index " + str(randInt))
        # randKey = list(accepting.keys())[randInt]
        # randKey = accepting[randInt]
        randKey = list(accepting[randInt]["bool"].keys())[0]
        randValues = accepting[randInt]["bool"][randKey]
        # Now we have the intersection, add it to the list
        list_intersections.append({
            **combination, 
            "intersection":accepting,
            "randEdit":{"key":randKey, "signals":randValues}
        })

    # Quick fix to add recovery references to the list of intersections
    print(" - Add recovery references to the list of intersections")
    references = {}
    recoveryKeyLength = {}
    for p_and_l in policies_and_locations:
        ref = 0
        policy = p_and_l[0]
        if policy not in references.keys():
            references[policy] = {}
        for location in p_and_l[1]:
            references[policy] = {**references[policy], location: ref}
            ref += 1
        recoveryKeyLength[policy] = len('{0:b}'.format(ref))

    # Get binary recoveryKeys
    # Stored in the "list_intersections" list1 under key "recoveryKey" for each row
    print(" - Add binary recovery keys")
    individualRecoveryKeys = {} # This one holds individual keys, this might be helpful on the compiler side
    for intersection in list_intersections:
        recoveryKey = ""
        for policy in policies:
            b = '{0:b}'.format(references[policy][intersection[policy]])
            # Pad with 0s as required to meet length
            toPad = recoveryKeyLength[policy] - len(b)
            b = "0" * toPad + b
            recoveryKey += b

            if policy not in individualRecoveryKeys.keys():
                individualRecoveryKeys[policy] = {}
            if intersection[policy] not in individualRecoveryKeys[policy].keys():
                individualRecoveryKeys[policy][intersection[policy]] = {}
            individualRecoveryKeys[policy][intersection[policy]] = b
            # individualRecoveryKeys[policy][intersection[policy]]["binary"] = "TODO"

        intersection["recoveryKey"]= recoveryKey 

    writeNewXML_two(originalXMLRoot, input_filename, output_filename, policies, alphabetTemplate, list_intersections, references, individualRecoveryKeys)

    return 

    # Now iterate through this list, pulling each set of acceptable from policies object
    rowNumber = 0
    lastPrinted = 100
    for row in rowsExample:
        # print(row)
        totalRows = len(rowsExample)
        rowNumber += 1
        # print(rowNumber / totalRows * 100, totalRows, rowNumber)
        if (int(rowNumber / totalRows * 100)) % 10 == 0:
            if (lastPrinted != (int(rowNumber / totalRows * 100))):
                print(int(rowNumber / totalRows * 100), "%\t", rowNumber, "of", totalRows)
                lastPrinted = int(rowNumber / totalRows * 100)
        
        acceptableSets = []
        for policy in row:
            if row[policy] == 0:
                print("Dont Care - Add things that dont violate the policy.. in this location..?")
            else:
                # print("Add", policy, row[policy]-1)#, policies[policy][row[policy]-1]["acceptableConditions"])
                acceptableSets.append(policies[policy][row[policy]-1]["acceptableConditions"])

        # Do an intersection
        intersection = acceptableSets[0]
        for i in range(1, len(acceptableSets)):
            intersection = getIntersection(intersection, acceptableSets[i])

        # print("Intersection:", end=" ")
        # pprint.pprint(intersection)
        
        # NOTE: This will fail when intersection is empty set! 
        # NOTE: The script currently ONLY supports CAPS LOCK inputs and outputs! A reason you may be here is because of that...!
        assert(len(intersection) > 0)
        # We are expecting this to occur for some examples, just need to handle it gracefully.
        # In some cases this assert will fail when the designer has created unenforceable policies
        # In other cases, the policies will never emit the two violationRef signals at the same time, thus this row/edit/enforcement action doesnt need to exist
    
        # TODO: Then do a minEdit
        selectedRecovery = intersection[list(intersection.keys())[0]] 

        # Get binary recoveryKeys
        recoveryKey = ""
        for policy in row:
            b = '{0:b}'.format(row[policy])
            # Pad with 0s as required to meet length
            toPad = recoveryKeyLength[policy] - len(b)
            b = "0" * toPad + b
            recoveryKey += b
        row["recoveryKey"] = recoveryKey 

        row["recovery"] = list(intersection.keys())[0]
        row["recoveryValue"] = intersection[list(intersection.keys())[0]]

    writeNewXML(originalXMLRoot, input_filename, output_filename, policies, alphabetTemplate, rowsExample)

###########################################################################

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("ERROR\nExpecting 2 arguments: project directory then project file.")
        print("For the AB example: python rtecomp/main.py AB AB\n")
        assert(len(sys.argv) == 3)
    projectDir = sys.argv[1]
    projectFile = sys.argv[2]

    # import cProfile
    # import re
    # cProfile.run("main(projectDir,projectFile)")

    main(projectDir, projectFile)

###########################################################################
