import random
import sys

# Clear the logs.txt file
with open('output/logs.txt', 'w') as file:
    pass

ALPHABET = ("A","C","G","T")

PATTERNS = (
    "AATTGA",
    "CGCTTAT",
    "GGACTAT",
    "TTATTCGTA"
)

VERBOSE = True

def RandomInt(start, end):
    return random.randint(start, end)

def GetRandomSymbol():
    return ALPHABET[RandomInt(0, 3)]

def GenerateRandomStringOfSymbols(stringLength):
    numberOfSymbols = RandomInt(1, stringLength)
    stringOfSymbols = ""
    for _ in range(numberOfSymbols):
        stringOfSymbols += GetRandomSymbol()
    return stringOfSymbols

def AddStringOfSymbolsAtIndex(pattern, stringOfSymbols, index):
    pattern = list(pattern)
    pattern[index:index] = stringOfSymbols
    return "".join(pattern)

def AddStringOfSymbolsAtStart(pattern, stringOfSymbols):
    printMessage(f"Initialising the sequence with {str(len(stringOfSymbols))} symbol(s)")
    return AddStringOfSymbolsAtIndex(pattern, stringOfSymbols, 0)

def AddStringOfSymbolsAtEnd(pattern, stringOfSymbols):
    endOfString = len(pattern)
    printMessage(f"Also adding the symbol(s) {str(stringOfSymbols)} at the end of the string")
    return AddStringOfSymbolsAtIndex(pattern, stringOfSymbols, endOfString)

# replaces a random number of symbols
def ReplaceSymbols(pattern):
    numberOfSymbolsToBeReplaced = RandomInt(0, 2)

    if numberOfSymbolsToBeReplaced == 0:
        printMessage("No symbols will be replaced/removed!")
        return pattern
    
    printMessage(f"There will be {str(numberOfSymbolsToBeReplaced)} symbol(s) replaced/removed")

    randomIndices = []
    pattern = list(pattern)
    patternLength = len(pattern)
    for _ in range(numberOfSymbolsToBeReplaced):
        SelectAndReplaceUniqueIndex(pattern, patternLength, randomIndices)

    pattern = "".join(pattern).replace("_", "")
    return pattern

# selects a random index and replaces the symbol at that index using ReplaceSymbolAtIndex()
def SelectAndReplaceUniqueIndex(pattern, patternLength, randomIndices):
    randomIndex = RandomInt(0, patternLength - 1)

    if randomIndex in randomIndices:
        SelectAndReplaceUniqueIndex(pattern, patternLength, randomIndices)
        return 
    
    ReplaceSymbolAtIndex(pattern, randomIndex)
    randomIndices.append(randomIndex)

# replaces the symbol at the index with a random symbol
# if the symbol at the index is the same as the random symbol, it replaces it with "_" instead
def ReplaceSymbolAtIndex(pattern, index):
    ramdomSymbol = GetRandomSymbol()

    if pattern[index] == ramdomSymbol: 
        printMessage(f"Removing the symbol at index: {str(index)}({pattern[index]})")
        pattern[index] = "_"
        return 
    
    printMessage(f"Replacing the symbol at index: {str(index)}({pattern[index]}) with {ramdomSymbol}")
    pattern[index] = ramdomSymbol
    return 

def SelectUniqueIndex(mainList, secondaryList):
    randomIndex = RandomInt(0, 49)

    if randomIndex in secondaryList:
        SelectUniqueIndex(mainList, secondaryList)
        return 
    
    secondaryList.append(randomIndex)

def ReplaceIndexWithSymbol(listOfIndices, listOfSymbols):
    for i in range(len(listOfIndices)):
        listOfIndices[i] = listOfSymbols[listOfIndices[i]]
        
    return listOfIndices

def printDatasets(datasetA, datasetB):
    sys.stdout = open('output/datasetA.txt', 'w')
    for i in range(len(datasetA)):
        print(datasetA[i])

    sys.stdout = open('output/datasetB.txt', 'w')
    for i in range(len(datasetB)):
        print(datasetB[i]) 
    
    sys.stdout = sys.__stdout__

def printMessage(message1, message2 = None):
    if VERBOSE: 
        if message2 is None:
            log(message1)
            return
        log(message1)
        log(message2)

def log(message, filename='output/logs.txt', mode='a'):
    with open(filename, mode) as file:
        file.write(message + '\n')
