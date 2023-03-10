
from parse import * # pip install parse
import pprint
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
    print('Unwinding ', conditions)
    unwound = {}
    print("At start are any more to unwind??", areAnyNone(conditions))
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
    print("Any more to unwind??", areAnyNone(unwound))
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
    clkConditions = {}
    a = parse("{}and{}", conditionStr.lower())
    # print("Did I find and?", a)
    if a is not None:
        # AND - we can parse at this level for a single condition
        # print(a[0], "AND", a[1])
        LHS = parse_singleSignal(a[0])
        RHS = parse_singleSignal(a[1])
        condition = alphabetTemplate.copy()
        if not isClockCondition(LHS["signal"]):
            condition[LHS["signal"]] = LHS["value"]
        else:
            condition[LHS["signal"]] = LHS["value"]
        if not isClockCondition(RHS["signal"]):
            condition[RHS["signal"]] = RHS["value"]
        else:
            condition[RHS["signal"]] = RHS["value"]

        # print(conditionStr, "becomes", condition)
        conditions = {**conditions, **unwindConditions({getKey(condition): condition})}

    else:
        # check for or
        a = parse("{}or{}", conditionStr.lower())
        if a is None:
            print("Problem parsing no brackets condition: ", conditionStr)
            if isClockCondition(conditionStr):

                print("Single Clk condition: ", conditionStr)
                
                # Assumption is that ONLY the absence of all signals is causing this
                allAbsent = alphabetTemplate.copy()
                for sig in allAbsent:
                    allAbsent[sig] = False
                # print("allAbsent", allAbsent)

                # conditions = {**conditions, **unwindConditions({getKey(allAbsent): allAbsent})}
                conditions = {getKey(allAbsent):allAbsent}
                return conditions, clkConditions

            elif isSingleSignal(conditionStr, alphabetTemplate):
                print("Single condition: ", conditionStr)
                single = parse_singleSignal(conditionStr)
                condition = alphabetTemplate.copy()
                condition[single["signal"]] = single["value"]
                conditions = {**conditions, **unwindConditions({getKey(condition): condition})}
                return conditions, clkConditions

            else:
                assert(False)
        print(a[0], "OR", a[1])

        LHS = parse_singleSignal(a[0])
        condition1 = alphabetTemplate.copy()
        if not isClockCondition(LHS["signal"]):
            condition1[LHS["signal"]] = LHS["value"]
        else:
            condition1[LHS["signal"]] = LHS["value"]
            # clkConditions[LHS["signal"]] = LHS["value"]
        conditions = {**conditions, **unwindConditions({getKey(condition1): condition1})}

        RHS = parse_singleSignal(a[1])
        condition2 = alphabetTemplate.copy()
        if not isClockCondition(RHS["signal"]):
            condition2[RHS["signal"]] = RHS["value"]
        else:
            condition2[RHS["signal"]] = RHS["value"]
            # clkConditions[RHS["signal"]] = RHS["value"]

        conditions = {**conditions, **unwindConditions({getKey(condition2): condition2})}
    
    print(conditionStr, "becomes", conditions, clkConditions)
    return conditions, clkConditions

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
    withoutClockConditions = {}
    for condition in conditions:
        print('hi2', condition, conditions)#[condition], len(alphabetTemplate))
        # conditionValue = {}
        # for value in conditions[condition]:
        #     if value in alphabetTemplate:
        #         conditionValue[value] = conditions[condition][value]
        # print(condition[0:len(alphabetTemplate)], conditionValue)
        withoutClockConditions[condition[0:len(alphabetTemplate)]] = conditions[condition]
    return withoutClockConditions

def stripClockConditionsFromKey(key, alphabetKeyLength):
    print("alphabetKeyLength:", alphabetKeyLength, "long, Key is", len(key), "long")
    return key[0:alphabetKeyLength]

def convertConditionToDictOfBools(conditionString, alphabetTemplate):
    # print(alphabetTemplate)
    print(conditionString)

    # Remove spaces
    a = conditionString.replace(" ", "")
    print("Original", a)
    
    # Count number of brackets
    left = a.count("(")
    right = a.count(")")
    assert(left == right, "Brackets must be matching")

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
        L, clkL = convertConditionToDictOfBools("("+LHS+")", alphabetTemplate)
        # R = parse_noBracketsCondition(RHS, alphabetTemplate)
        R, clkR = convertConditionToDictOfBools("("+RHS+")", alphabetTemplate)

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
        
        clk = {}
    else:
        print(b, b[0])
        topCondition, clk = parse_noBracketsCondition(b[0], alphabetTemplate)

    print("Returning: ", topCondition, "and clk", clk)
    return topCondition, clk

def getAcceptableTransitions(violationConditions, alphabetTemplate):
    violationConditionsNoClocks = removeClockConditionKeys(violationConditions, alphabetTemplate)
    print("with clocks:", violationConditions)
    print("without clocks:", violationConditionsNoClocks)
    any = alphabetTemplate.copy()
    acceptableTransitions = {}
    allConditions = unwindConditions({getKey(any): any})
    for condition in allConditions: # TODO: Come up with a way to compare while ignoring any clock conditions?
        if condition in violationConditionsNoClocks:
            pass
        else:
            acceptableTransitions[condition] = allConditions[condition]

    print("Acceptable Transitions (", len(acceptableTransitions), ") -", acceptableTransitions)
    print("Violating Transitions (", len(violationConditions), ") -", violationConditions)
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

def writeNewXML(root, input_filename, output_filename, policies, alphabetTemplate, rowsExample):
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

    # Remove ALL existing violation transitions
    for tag in bs_data.find_all("PTransition"):
        for dest in tag.find_all("Destination", string="violation"):
            # print(dest)
            tag.extract()

    # Add ALL NEW recoveries
    for policy in policies:
        recoveries = policies[policy]
        for recovery in recoveries:
            # print(recoveries[recovery])
            # print(recoveries[recovery]["policy"])

            policyTag = bs_data.find("Policy", {"Name":recovery["policy"]})

            pt = bs_data.new_tag("PTransition")
            pt.append(bs_data.new_tag("Source"))
            pt.Source.append(recovery["location"])

            pt.append(bs_data.new_tag("Destination"))
            pt.Destination.append("violation")

            pt.append(bs_data.new_tag("Condition"))
            # Need to add clock conditions here IFF RELEVANT
            print(recovery["violatingCondition"], recovery["violatingConditionString"])
            if isClockCondition(recovery["violatingConditionString"]):
                # TODO: Extract clock condition PROPERLY (the current implementation will only work for a single)
                clockCondition = recovery["violatingConditionString"]
                pt.Condition.append("("+convertBinaryStringToTextCondition(recovery["violatingCondition"], alphabetTemplate) + " and " + clockCondition + ")")
            else:
                pt.Condition.append(convertBinaryStringToTextCondition(recovery["violatingCondition"], alphabetTemplate))
            # input("Any key to continue")

            recoveryRefTag = bs_data.new_tag("RecoveryReference")
            recoveryRefTag.append(str(recovery["violationRef"]))
            pt.append(recoveryRefTag)



            policyTag.Machine.append(pt)

    topEnfFnTag = bs_data.find("EnforcedFunction")
    selectLUTTag = bs_data.new_tag("SelectLUT")
    for row in rowsExample:
        rowTag = bs_data.new_tag("Row")

        recoveryTag = bs_data.new_tag("Recovery")
        recoveryTag.append(row["recovery"])
        recoveryKeyTag = bs_data.new_tag("RecoveryKey")
        recoveryKeyTag.append(row["recoveryKey"])

        for k in row:
            if (k != "recovery") & (k != "recoveryKey"):
                # Policy
                pRefTag = bs_data.new_tag("PolicyRef", Policy=str(k), RecoveryReference=str(row[k]))
                pRefTag = bs_data.new_tag("PolicyRef", Policy=str(k), RecoveryReference=str(row[k]))
                rowTag.append(pRefTag)

        # recoveryTag = bs_data.new_tag("Row")

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

import xml.etree.ElementTree as ET

print("======================================")
print(" READING & PARSING EXISTING XML FILE")
print("======================================")

# Passing the path of the
# xml document to enable the
# parsing process
projectName = "ab"
input_filename = "example/"+projectName+"/"+projectName+".xml"
output_filename = "example/"+projectName+"/"+projectName+"_modified.xml"
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
print(" COLLECTING ALL VIOLATING TRANSITIONS")
print("==========================================")

# Find each policies violating transitions
policies = {}
for policy in originalXMLRoot.iter("Policy"):
    allViolationTransitions = []
    policyViolationCount = 0
    for transition in policy.iter('PTransition'):
        for child in transition.iter('Recover'):
            print(policy.attrib.get("Name"), " ", transition.find("Source").text, " to ", transition.find("Destination").text, " on ", transition.find("Condition").text, ". Recovers with ", child.find("VarName").text, child.find("Value").text)
            violationConditions, _ = convertConditionToDictOfBools(transition.find("Condition").text, alphabetTemplate)
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
                    "violatingCondition":stripClockConditionsFromKey(violatingCondition, alphabetKeyLength),
                    "acceptableConditions":acceptable
                })
            # input("Press any key to continue.")
    policies[policy.attrib.get("Name")] = allViolationTransitions

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

# Create template to be used as rows (each policy should have a column, which will hold the violation reference)
rowTemplate = {}
for policy in policies:
    rowTemplate[policy] = 1 # Changed 0 here to 1 to remove don't cares

numberRowsExpected = 1
recoveryKeyLength = {}
for policy in policies:
    numberRowsExpected = numberRowsExpected * (len(policies[policy])) # Removed +1 here to remove don't cares
    recoveryKeyLength[policy] = len('{0:b}'.format(len(policies[policy])))

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

assert(len(rowsExample) == numberRowsExpected)

# List of dictionaries with each policy and violation refs
import pprint
# pprint.pprint(rowsExample)

print("=============================================")
print(" PRE-CRUNCHING EDITS FOR VIOLATION REF COMBO")
print("=============================================")

# Now iterate through this list, pulling each set of acceptable from policies object
for row in rowsExample:
    print(row)
    acceptableSets = []
    for policy in row:
        if row[policy] == 0:
            print("Dont Care - Add things that dont violate the policy.. in this location..?")
        else:
            print("Add", policy, row[policy]-1)#, policies[policy][row[policy]-1]["acceptableConditions"])
            acceptableSets.append(policies[policy][row[policy]-1]["acceptableConditions"])

    # Do an intersection
    intersection = acceptableSets[0]
    for i in range(1, len(acceptableSets)):
        intersection = getIntersection(intersection, acceptableSets[i])

    print("Intersection:", end=" ")
    pprint.pprint(intersection)
    
    # NOTE: This will fail when intersection is empty set! 
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

writeNewXML(originalXMLRoot, input_filename, output_filename, policies, alphabetTemplate, rowsExample)
