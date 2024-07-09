import mainHelper as h
import numpy as np
import sys

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
            h.printMessage(f"Result: {self.string}\n", "Doing this another 49 times...\n")
            self.string = ""
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


def global_alignment(seq1, seq2, gap_penalty, mismatch_penalty):
    sys.stdout = open('m.txt', 'w')
    n = len(seq1)
    m = len(seq2)
    dp = np.zeros((n+1, m+1))

    for i in range(1, n+1):
        dp[i][0] = i * gap_penalty
    for j in range(1, m+1):
        dp[0][j] = j * gap_penalty

    for i in range(1, n+1):
        for j in range(1, m+1):
            match = dp[i-1][j-1] + (1 if seq1[i-1] == seq2[j-1] else mismatch_penalty)
            delete = dp[i-1][j] + gap_penalty
            insert = dp[i][j-1] + gap_penalty
            dp[i][j] = max(match, delete, insert)

    alignment1, alignment2 = '', ''
    i, j = n, m
    while i > 0 and j > 0:
        current_score = dp[i][j]
        if current_score == dp[i-1][j-1] + (1 if seq1[i-1] == seq2[j-1] else mismatch_penalty):
            alignment1 = seq1[i-1] + alignment1
            alignment2 = seq2[j-1] + alignment2
            i -= 1
            j -= 1
        elif current_score == dp[i-1][j] + gap_penalty:
            alignment1 = seq1[i-1] + alignment1
            alignment2 = '-' + alignment2
            i -= 1
        else:
            alignment1 = '-' + alignment1
            alignment2 = seq2[j-1] + alignment2
            j -= 1

    while i > 0:
        alignment1 = seq1[i-1] + alignment1
        alignment2 = '-' + alignment2
        i -= 1

    while j > 0:
        alignment1 = '-' + alignment1
        alignment2 = seq2[j-1] + alignment2
        j -= 1

    return alignment1, alignment2

def multiple_sequence_alignment(sequences, gap_penalty, mismatch_penalty):
    alignments = [sequences[0]]
    for seq in sequences[1:]:
        new_alignments = []
        for aligned_seq in alignments:
            aligned1, aligned2 = global_alignment(aligned_seq, seq, gap_penalty, mismatch_penalty)
            new_alignments.append(aligned1)
            new_alignments.append(aligned2)
        alignments = new_alignments
    return alignments

# Αν τα ΑΜ των μελών της ομάδας καταλήγουν σε περιττό ψηφίο τότε α=1, αλλιώς α=2
alpha = 2  # Αντικαταστήστε το με 2 αν χρειάζεται
gap_penalty = -alpha
mismatch_penalty = -alpha / 2

aligned_sequences = multiple_sequence_alignment(sg.datasetA, gap_penalty, mismatch_penalty)
for s in aligned_sequences:
    print(s, len(s))
