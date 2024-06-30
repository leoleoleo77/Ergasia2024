import mainHelper as h

class StringGenerator:

    def __init__(self):
        self.string = ""
        self.allStrings = []
        self.datasetA = []
        self.datasetB = []

    def Generate50Strings(self):
        for _ in range(50):
            h.printMessage("-STEP A:\n")
            self.string = h.AddStringOfSymbolsAtStart(self.string, h.GenerateRandomStringOfSymbols(3))
            h.printMessage(f"Result: {self.string}\n", "-STEP B:\n")

            for pattern in h.PATTERNS:
                h.printMessage(f"For the Pattern {pattern},")
                pattern = h.ReplaceSymbols(pattern)
                h.printMessage(f"Result: {pattern}\n")
                self.string += pattern

            h.printMessage("-STEP C:\n", "Adding all the patterns to the initial string")
            self.string = h.AddStringOfSymbolsAtEnd(self.string, h.GenerateRandomStringOfSymbols(2))
            self.allStrings.append(self.string)
            self.string = ""
            h.printMessage(f"Result: {self.string}\n", "Doing this another 49 times...\n")
            h.VERBOSE = False
    
    def FillDatasets(self):
        for _ in range(15):
            h.SelectUniqueIndex(self.allStrings, self.datasetA)
        for i in range(50):
            if i not in self.datasetA:
                self.datasetB.append(i)
        self.datasetA = h.ReplaceIndexWithSymbol(self.datasetA, self.allStrings)
        self.datasetB = h.ReplaceIndexWithSymbol(self.datasetB, self.allStrings)
        h.printDatasets(self.datasetA, self.datasetB)
            

sg = StringGenerator()
sg.Generate50Strings()
sg.FillDatasets()