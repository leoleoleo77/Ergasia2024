import Helper as h

class SequenceGenerator:

    def __init__(self):
        self.sequence = ""
        self.allSequences = []
        self.datasetA = []
        self.datasetB = []
        self.Generate50Sequences()
        self.FillDatasets()

    def Generate50Sequences(self):
        for _ in range(50):
            h.printMessage("-STEP A:\n")
            self.sequence = h.AddStringOfSymbolsAtStart(self.sequence, h.GenerateRandomStringOfSymbols(3))
            h.printMessage(f"Result: {self.sequence}\n", "-STEP B:\n")

            for pattern in h.PATTERNS:
                h.printMessage(f"For the Pattern {pattern},")
                pattern = h.ReplaceSymbols(pattern)
                h.printMessage(f"Result: {pattern}\n")
                self.sequence += pattern

            h.printMessage("-STEP C:\n", "Adding all the patterns to the initial sequence")
            self.sequence = h.AddStringOfSymbolsAtEnd(self.sequence, h.GenerateRandomStringOfSymbols(2))
            self.allSequences.append(self.sequence)
            h.printMessage(f"Result: {self.sequence}\n", "Doing this another 49 times and scattering the results between datasetA & datasetB...\n")
            self.sequence = ""
            h.VERBOSE = False
    
    def FillDatasets(self):
        for _ in range(15):
            h.SelectUniqueIndex(self.allSequences, self.datasetA)
        for i in range(50):
            if i not in self.datasetA:
                self.datasetB.append(i)
        self.datasetA = h.ReplaceIndexWithSymbol(self.datasetA, self.allSequences)
        self.datasetB = h.ReplaceIndexWithSymbol(self.datasetB, self.allSequences)
        h.printDatasets(self.datasetA, self.datasetB)
