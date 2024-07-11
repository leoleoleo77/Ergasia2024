import random
import numpy as np
import sys

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
    printMessage(f"Initialising the string with {str(len(stringOfSymbols))} symbol(s)")
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
        #pattern.pop(index)
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
            print(message1)
            return
        print(message1)
        print(message2)

def initializeScoreMatrix(n, m, gap):
    scoreMatrix = np.zeros((n + 1, m + 1))

    for i in range(n + 1):
        scoreMatrix[i][0] = i * gap
    for j in range(m + 1):
        scoreMatrix[0][j] = j * gap
    
    return scoreMatrix

def calculateScoreMatrix(n, m, seq1, seq2, match, mismatch, gap):
    scoreMatrix = initializeScoreMatrix(n, m, gap)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diagonal_top_left_score = scoreMatrix[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            top_score = scoreMatrix[i - 1][j] + gap
            left_score = scoreMatrix[i][j - 1] + gap
            scoreMatrix[i][j] = max(diagonal_top_left_score, top_score, left_score)
    
    return scoreMatrix

def backtracking(n, m, seq1, seq2, match, mismatch, gap, scoreMatrix):
    align1 = ""
    align2 = ""
    i, j = n, m
    while i > 0 or j > 0:
        score_current = scoreMatrix[i][j]
        score_diagonal = scoreMatrix[i - 1][j - 1]
        # score_up = scoreMatrix[i][j - 1]
        score_left = scoreMatrix[i - 1][j]
        
        # A diagonal arrow represents a match or mismatch, 
        # so the letter of the column and the letter of the row of the origin cell will align.
        if i > 0 and j > 0 and score_current == score_diagonal + (match if seq1[i - 1] == seq2[j - 1] else mismatch):
            align1 += seq1[i - 1]
            align2 += seq2[j - 1]
            i -= 1
            j -= 1
        
        # A horizontal or vertical arrow represents an indel.
        # Vertical arrows will align a gap ("-") to the letter of the row (the "side" sequence),
        # horizontal arrows will align a gap to the letter of the column (the "top" sequence).
        elif i > 0 and score_current == score_left + gap:
            align1 += seq1[i - 1]
            align2 += "-"
            i -= 1
        else:
            align1 += "-"
            align2 += seq2[j - 1]
            j -= 1

    # Reverse the strings.
    align1, align2 = align1[::-1], align2[::-1]
    return align1, align2

