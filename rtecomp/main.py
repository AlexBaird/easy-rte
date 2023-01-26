
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

def parse_noBracketsCondition(conditionStr, alphabetTemplate, alphabetKeyLength):
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
        condition[LHS["signal"]] = LHS["value"]
        condition[RHS["signal"]] = RHS["value"]
        # print(conditionStr, "becomes", condition)
        conditions = {**conditions, **unwindConditions({getKey(condition): condition})}
        # print(conditions)

    else:
        # check for or
        a = parse("{}or{}", conditionStr.lower())
        if a is None:
            print("Problem parsing no brackets condition: ", conditionStr)
            assert(False)
        print(a[0], "OR", a[1])

        LHS = parse_singleSignal(a[0])
        condition1 = alphabetTemplate.copy()
        condition1[LHS["signal"]] = LHS["value"]
        conditions = {**conditions, **unwindConditions({getKey(condition1): condition1})}

        RHS = parse_singleSignal(a[1])
        condition2 = alphabetTemplate.copy()
        condition2[RHS["signal"]] = RHS["value"]
        conditions = {**conditions, **unwindConditions({getKey(condition2): condition2})}
    
    print(conditionStr, "becomes", conditions, "\n\n")
    return conditions

def getCharacterRepeated(count, char):
    repeated = ""
    for number in range(0, count) : repeated = repeated + str(char)
    return repeated


def convertConditionToListOfBools(conditionString, alphabetTemplate, alphabetKeyLength):
    print(alphabetTemplate)
    print(conditionString)

    # Remove spaces
    a = conditionString.replace(" ", "")
    print("Original", a)

    # Remove topmost brackets
    b = parse("({})", a)
    count = 0
    while True:
        # Keep going till all top brackets gone
        if parse("({})", b[0]) is not None:
            print("Part:", b[0])
            b = parse("({})", b[0])
            count += 1
        else:
            break
    
    print("Top brackets removed:", count, b[0])

    if count > 0:
        # Separate into LHS, condition and RHS
        # Example: !AandB)or(AandB 
        # Becomes: <Result ('!AandB', 'or', 'AandB') {}>
        formatString = "{}" + getCharacterRepeated(count, ")") + "{}" + getCharacterRepeated(count, "(") + "{}"
        print(formatString)
        topCondition = parse(formatString, b[0])
    else:
        print(b, b[0])
        topCondition = parse_noBracketsCondition(b[0], alphabetTemplate, alphabetKeyLength)

    print(topCondition)

    # Condition is either "AND" or "OR"
    print("top condition: ", topCondition)
    condition = topCondition[1].lower()
    if (condition == "or"):
        # OR means TWO transitions to violation
        print("OR")
        # TODO: Recursively find all transitions - keep going till you have ONLY ANDS in a list/table
        LHS = topCondition[0]
        RHS = topCondition[2]

    elif (condition == "and"):
        # AND means single transition
        print("AND")


    LHS = topCondition[0]
    RHS = topCondition[2]
    print(LHS, parse_isOR(LHS), parse_isAND(LHS))
    print(RHS, parse_isOR(RHS), parse_isAND(RHS))
    return

###########################################################################

import xml.etree.ElementTree as ET

# Passing the path of the
# xml document to enable the
# parsing process
tree = ET.parse('example/abc5/abc5.xml')
 
# getting the parent tag of
# the xml document
root = tree.getroot()
 
# printing the root (parent) tag
# of the xml document, along with
# its memory location
print("Enforced Function: ", root.attrib.get("Name"))

alphabetTemplate, alphabetKeyLength = convertInterfaceToBoolDict(root)

# root.tag
# root.attrib
# for child in root:
#     print(child.tag, child.attrib)
#     for childchild in child:
#         print("\t", childchild.tag, childchild.attrib)

# Find each policies violating transitions
for policy in root.iter("Policy"):
    for transition in policy.iter('PTransition'):
        for child in transition.iter('Recover'):
            print(policy.attrib.get("Name"), " ", transition.find("Source").text, " to ", transition.find("Destination").text, " on ", transition.find("Condition").text, ". Recovers with ", child.find("VarName").text, child.find("Value").text)
            convertConditionToListOfBools(transition.find("Condition").text, alphabetTemplate, alphabetKeyLength)
            exit()