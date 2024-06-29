import mainHelper as h

class String:
    def __init__(self):
        self.string = ""

    def temp(self):

        if h.VERBOSE:
            print("-STEP A:\n")
        self.string = h.AddStringOfSymbolsAtStart(self.string, h.GenerateRandomStringOfSymbols(3))

        if h.VERBOSE:
                print("Result: " + self.string + "\n")
                print("-STEP B:\n")
        for pattern in h.PATTERNS:

            if h.VERBOSE:
                print(f"For the Pattern {pattern},")

            pattern = h.ReplaceSymbols(pattern)

            if h.VERBOSE:
                print("Result: " + pattern + "\n")
        
            self.string += pattern

        if h.VERBOSE:
            print("-STEP C:\n")
            print("Adding all the patterns to the initial string")

        self.string = h.AddStringOfSymbolsAtEnd(self.string, h.GenerateRandomStringOfSymbols(2))
        if h.VERBOSE:
            print(f"Result: {self.string}\n")



myString = String()
myString.temp()