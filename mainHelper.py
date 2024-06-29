import random

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

def GenerateRandomStringOfSymbols(n):
    numberOfSymbols = RandomInt(1, n)
    stringOfSymbols = ""

    for _ in range(numberOfSymbols):
        stringOfSymbols += GetRandomSymbol()

    return stringOfSymbols

def AddStringOfSymbolsAtIndex(pattern, stringOfSymbols, index):
    pattern = list(pattern)
    pattern[index:index] = stringOfSymbols
    return "".join(pattern)

def AddStringOfSymbolsAtStart(pattern, stringOfSymbols):
    if VERBOSE:
        print("Initialising the string with " + str(len(stringOfSymbols)) + " symbol(s)")
    return AddStringOfSymbolsAtIndex(pattern, stringOfSymbols, 0)

def AddStringOfSymbolsAtEnd(pattern, stringOfSymbols):
    endOfString = len(pattern)
    if VERBOSE:
        print(f"Also adding the symbol(s) {str(stringOfSymbols)} at the end of the string")
    return AddStringOfSymbolsAtIndex(pattern, stringOfSymbols, endOfString)

def ReplaceSymbols(pattern):
    numberOfSymbolsToBeReplaced = RandomInt(0, 2)

    if numberOfSymbolsToBeReplaced == 0:
        if VERBOSE:
            print("No symbols will be replaced/removed!")
        return pattern
    
    if VERBOSE:
            print("There will be " + str(numberOfSymbolsToBeReplaced)+ " symbol(s) replaced/removed")
    randomIndices = []
    pattern = list(pattern)
    for _ in range(numberOfSymbolsToBeReplaced):
        SelectAndReplaceUniqueIndex(pattern, randomIndices
        )

    pattern = "".join(pattern)
    return pattern

def SelectAndReplaceUniqueIndex(pattern, randomIndices):
    randomIndex = RandomInt(0, len(pattern) - 1)

    if randomIndex in randomIndices:
        SelectAndReplaceUniqueIndex(pattern, randomIndices)
        return 
    
    ReplaceSymbolAtIndex(pattern, randomIndex)
    randomIndices.append(randomIndex)

def ReplaceSymbolAtIndex(pattern, index):
    ramdomSymbol = GetRandomSymbol()

    if pattern[index] == ramdomSymbol: 
        if VERBOSE:
            print("Removing the symbol at index: " + str(index) + "(" + pattern[index] + ")")
        pattern.pop(index)
        return 
    
    if VERBOSE:
            print(f"Replacing the symbol at index: {str(index)}({pattern[index]}) with {ramdomSymbol}")
    pattern[index] = ramdomSymbol
    return 