
from parse import * # pip install parse

# from bs4 import BeautifulSoup
 
# # Reading the data inside the xml
# # file to a variable under the name
# # data
# with open('example/abc5/abc5.xml', 'r') as f:
#     data = f.read()
 
# # Passing the stored data inside
# # the beautifulsoup parser, storing
# # the returned object
# Bs_data = BeautifulSoup(data, "xml")
 
# # Finding all instances of tag
# # `unique`
# b_unique = Bs_data.find_all('Recover')
 

###########################################################################
# Helper Functions

def convertInterfaceToBoolDict(root):
    alphabet = {}
    keyLength = 0 # This will determine the length of the key that we will use to capture the dictionary
    for alphabetItem in root.iter("Interface"):
        for child in alphabetItem:
            if child.get("Type") != "bool":
                print("Support for boolean interfaces only!")
                exit()
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
    print('Unwinding ', conditions)
    unwound = {}
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
    print("Unwound to", unwound)
    return unwound

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

def parse_noBracketsCondition(conditionStr, alphabetTemplate):
    assert(parse_validateNoBrackets(conditionStr))
    conditions = {}
    a = parse("{}and{}", conditionStr.lower())
    # print(a)
    if a is not None:
        # and found - we can parse at this level for a single condition
        # print(a[0], "AND", a[1])
        LHS = parse_singleSignal(a[0])
        RHS = parse_singleSignal(a[1])
        condition = alphabetTemplate.copy()
        if not isClockCondition(LHS["signal"]):
            condition[LHS["signal"]] = LHS["value"]
        if not isClockCondition(RHS["signal"]):
            condition[RHS["signal"]] = RHS["value"]
        # print(conditionStr, "becomes", condition)
        conditions = {**conditions, **unwindConditions({getKey(condition): condition})}
        # print(conditions)

    else:
        # check for or
        a = parse("{}or{}", conditionStr.lower())
        if a is None:
            print("Problem parsing no brackets condition: ", conditionStr)
            if isClockCondition(conditionStr):
                print("Clock condition with nothing else. Any signal will avoid violation transition.")
                # any = alphabetTemplate.copy()
                # conditions = {**conditions, **unwindConditions({getKey(any): any})}
                return conditions
            elif isSingleSignal(conditionStr, alphabetTemplate):
                print("Single condition: ", conditionStr)
                single = parse_singleSignal(conditionStr)
                condition = alphabetTemplate.copy()
                condition[single["signal"]] = single["value"]
                conditions = {**conditions, **unwindConditions({getKey(condition): condition})}
                return conditions

            else:
                assert(False)
        print(a[0], "OR", a[1])

        LHS = parse_singleSignal(a[0])
        condition1 = alphabetTemplate.copy()
        if not isClockCondition(LHS["signal"]):
            condition1[LHS["signal"]] = LHS["value"]
        conditions = {**conditions, **unwindConditions({getKey(condition1): condition1})}

        RHS = parse_singleSignal(a[1])
        condition2 = alphabetTemplate.copy()
        if not isClockCondition(RHS["signal"]):
            condition2[RHS["signal"]] = RHS["value"]
        conditions = {**conditions, **unwindConditions({getKey(condition2): condition2})}
    
    print(conditionStr, "becomes", conditions)
    return conditions

def getCharacterRepeated(count, char):
    repeated = ""
    for number in range(0, count) : repeated = repeated + str(char)
    return repeated

def getIntersection(first, second):
    intersection = {}
    for f in first:
        if f in second:
            # print("Found a match")
            intersection[f] = second[f]
        # else:
            # print("Found NO match", first[f])
    # print("First: ", first)
    # print("Second: ", second)
    # print("Intersection: ", intersection)
    return intersection

def convertConditionToDictOfBools(conditionString, alphabetTemplate):
    # print(alphabetTemplate)
    print(conditionString)

    # Remove spaces
    a = conditionString.replace(" ", "")
    print("Original", a)

    # Remove topmost brackets
    b = parse("({})", a)
    count = 0
    if b is not None:
        while True:
            # Keep going till all top brackets gone
            if parse("({})", b[0]) is not None:
                print("Part:", b[0])
                b = parse("({})", b[0])
                count += 1
            else:
                break
    
        print("Top brackets removed:", count, b[0])
    else: 
        b=[]
        print("No brackets to remove..?", a)
        b.append(a)

    if count > 0:
        # Separate into LHS, condition and RHS
        # Example: !AandB)or(AandB 
        # Becomes: <Result ('!AandB', 'or', 'AandB') {}>
        formatString = "{}" + getCharacterRepeated(count, ")") + "{}" + getCharacterRepeated(count, "(") + "{}"
        print(formatString)
        topCondition = parse(formatString, b[0])

        print(topCondition)
        
        # TODO: Recursively find all transitions - keep going till you have ONLY ANDS in a list/table

        LHS = topCondition[0]
        RHS = topCondition[2]

        # print("LHS:", LHS, "RHS:", RHS)
        # L = parse_noBracketsCondition(LHS, alphabetTemplate)
        L = convertConditionToDictOfBools("("+LHS+")", alphabetTemplate)
        # R = parse_noBracketsCondition(RHS, alphabetTemplate)
        R = convertConditionToDictOfBools("("+RHS+")", alphabetTemplate)

        # Condition is either "AND" or "OR"
        print("top condition: ", topCondition)
        condition = topCondition[1].lower()
        if (condition == "or"):
            # OR means APPEND sets of conditions for transition to violation
            print("OR")
            topCondition = {**L, **R}
        elif (condition == "and"):
            # AND means INTERSECTION of sets of conditions for transition to violation
            print("AND")
            topCondition = getIntersection(L, R)

    else:
        print(b, b[0])
        topCondition = parse_noBracketsCondition(b[0], alphabetTemplate)

    print("Returning: ", topCondition)
    return topCondition

def getAcceptableTransitions(violationConditions, alphabetTemplate):
    any = alphabetTemplate.copy()
    acceptableTransitions = {}
    allConditions = unwindConditions({getKey(any): any})
    for condition in allConditions:
        print(condition, violationConditions)
        if condition in violationConditions:
            pass
        else:
            acceptableTransitions[condition] = allConditions[condition]

    print("Acceptable Transitions: ", acceptableTransitions)
    assert(len(acceptableTransitions) + len(violationConditions) == len(allConditions))
    return acceptableTransitions

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


def writeNewXML(root, output_filename, recoveries, alphabetTemplate):
    from bs4 import BeautifulSoup

    # Reading data from the xml file
    with open('example/abcd/abcd.xml', 'r') as f:
        data = f.read()

    # Passing the data of the xml
    # file to the xml parser of
    # beautifulsoup
    bs_data = BeautifulSoup(data, features='xml')

    # Remove ALL existing violation transitions
    for tag in bs_data.find_all("PTransition"):
        for dest in tag.find_all("Destination", string="violation"):
            # print(dest)
            tag.extract()

    # Add ALL NEW recoveries
    for recovery in recoveries:
        # print(recoveries[recovery])
        # print(recoveries[recovery]["policy"])

        policy = bs_data.find("Policy", {"Name":recoveries[recovery]["policy"]})
        
        pt = bs_data.new_tag("PTransition")
        pt.append(bs_data.new_tag("Source"))
        pt.Source.append(recoveries[recovery]["location"])

        pt.append(bs_data.new_tag("Destination"))
        pt.Destination.append("violation")

        pt.append(bs_data.new_tag("Condition"))
        pt.Condition.append(convertBinaryStringToTextCondition(recoveries[recovery]["violatingCondition"], alphabetTemplate))

        pt.append(bs_data.new_tag("Recover"))

        recoveriesText = convertBinaryRecoveryStringToTextListRecovery(recoveries[recovery]["recovery"], alphabetTemplate)
        print(recoveriesText)
        for recoveryText in recoveriesText:
            # print(recoveryText["VarName"], recoveryText["Value"])
            a = bs_data.new_tag("VarName")
            a.append(recoveryText["VarName"])
            pt.Recover.append(a)
            b = bs_data.new_tag("Value")
            b.append(recoveryText["Value"])
            pt.Recover.append(b)

        policy.Machine.append(pt)

    # Output the contents of the
    # modified xml file
    with open(output_filename, "w") as f2:
        f2.write(str(bs_data))
        f2.close()
        
###########################################################################

import xml.etree.ElementTree as ET

# Passing the path of the
# xml document to enable the
# parsing process
filename = "example/abcd/abcd.xml"
output_filename = "example/abcd/abcd_modified.xml"
# tree = ET.parse('example/abc5/abc5.xml')
tree = ET.parse(filename)
 
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

# Find each policies violating transitions
policies = {}
for policy in originalXMLRoot.iter("Policy"):
    allViolationTransitions = []
    policyViolationCount = 0
    for transition in policy.iter('PTransition'):
        for child in transition.iter('Recover'):
            print(policy.attrib.get("Name"), " ", transition.find("Source").text, " to ", transition.find("Destination").text, " on ", transition.find("Condition").text, ". Recovers with ", child.find("VarName").text, child.find("Value").text)
            violationConditions = convertConditionToDictOfBools(transition.find("Condition").text, alphabetTemplate)
            print(policy.attrib.get("Name"), " ", transition.find("Source").text, " to ", transition.find("Destination").text, " on ", transition.find("Condition").text, ". Recovers with ", child.find("VarName").text, child.find("Value").text)
            print("Violation Conditions: ", violationConditions)
            acceptable = getAcceptableTransitions(violationConditions, alphabetTemplate)

            for violatingCondition in violationConditions:
                # Put each violating signal set into table, [policy, reference, location, A, B, C, acceptable resolutions] 
                policyViolationCount += 1
                allViolationTransitions.append({
                    "policy":policy.attrib.get("Name"),
                    "violationRef":policyViolationCount,
                    "location":transition.find("Source").text,
                    "violatingConditionString":transition.find("Condition").text,
                    "violatingCondition":violatingCondition,
                    "acceptableConditions":acceptable
                })
            # input("Press any key to continue.")
    policies[policy.attrib.get("Name")] = allViolationTransitions

def addRecovery(recoveries, transitionInfo, recovery):
    recoveries[transitionInfo["policy"]+"-"+transitionInfo["location"]+"-"+transitionInfo["violatingCondition"]] = {
        "policy":transitionInfo["policy"],
        "location":transitionInfo["location"],
        "violatingConditionString":transitionInfo["violatingConditionString"],
        "violatingCondition":transitionInfo["violatingCondition"],
        "recovery":recovery
    }
    return

recoveries = {}
for policy in policies:
    # setsToIntersect.append(policies[policy])
    print("Policy:", policy)
    for violatingTransition in policies[policy]:
        # print("Transition:", violatingTransition["violatingCondition"])
        setsToIntersect = []
        violatingTransitionsToRecover = []
        setsToIntersect.append(policies[policy])
        violatingTransitionsToRecover.append(violatingTransition)
        for otherPolicy in policies:
            if policy != otherPolicy:
                for otherViolatingTransition in policies[otherPolicy]:
                    if violatingTransition["violatingCondition"] == otherViolatingTransition["violatingCondition"]:
                        setsToIntersect.append(policies[otherPolicy])
                        violatingTransitionsToRecover.append(otherViolatingTransition)
        intersectingRecoveries = setsToIntersect[0][0]["acceptableConditions"]
        # print("all: ", len(intersectingRecoveries))
        for i in range(1, len(setsToIntersect)):
            # print("Intersection")
            intersectingRecoveries = getIntersection(intersectingRecoveries, setsToIntersect[i][0]["acceptableConditions"])
        # print("intersecting: ", len(intersectingRecoveries))
        # pprint.pprint(intersectingRecoveries)

        # First Edit TODO: Replace with minEdit
        selectedRecovery = None
        for recovery in intersectingRecoveries:
            canUse = True
            for checkPolicy in policies:
                if checkPolicy != policy:
                    for checkViolatingTransition in policies[checkPolicy]:
                        # print("Checking - ", recovery, "against", checkPolicy)
                        if recovery == checkViolatingTransition["violatingCondition"]:
                            canUse = False # TODO: Replace with add to list then later perform MIN calculation to select min-edit
                            break
            if canUse:
                selectedRecovery = recovery
                break

        assert(selectedRecovery is not None)
        print("\tSelected Recovery:", selectedRecovery, "for", violatingTransition["policy"]+"-"+violatingTransition["location"]+"-"+violatingTransition["violatingCondition"])
        for vt in violatingTransitionsToRecover:
            if vt["policy"]+"-"+vt["location"]+"-"+vt["violatingCondition"] not in recoveries:
                print("\t\tAdded Recovery:", selectedRecovery, "for", vt["policy"]+"-"+vt["location"]+"-"+vt["violatingCondition"])
                addRecovery(recoveries, vt, selectedRecovery)

import pprint
pprint.pprint(recoveries)
print(len(recoveries))

writeNewXML(originalXMLRoot, output_filename, recoveries, alphabetTemplate)
