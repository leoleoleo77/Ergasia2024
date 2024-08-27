import numpy as np
import pandas as pd
import Helper as h

MATCH = 1
MISMATCH = -1
GAP = -2

class ScoreMatrix:

    VERBOSE = True

    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2
        self.seqScore = 0

        self.log(f"Comparing the sequences:\n{self.seq1}\n{self.seq2}\n")
        self.optimal_alignment()
        self.log(f"Aligned:\n{self.seq1}\n{self.seq2}\n")
        ScoreMatrix.VERBOSE = False

    def initialize_score_matrix(self, n, m):
        self.scoreMatrix = np.zeros((n + 1, m + 1))

        for i in range(n + 1):
            self.scoreMatrix[i][0] = i * GAP
        for j in range(m + 1):
            self.scoreMatrix[0][j] = j * GAP
        self.log("Initializing the Score Matrix:", self.scoreMatrix)
    
    def calculate_score_matrix(self, n, m):
        self.initialize_score_matrix(n, m)

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                diag = self.scoreMatrix[i - 1][j - 1] + self.score(i, j)
                left = self.scoreMatrix[i][j - 1] + GAP
                top = self.scoreMatrix[i - 1][j] + GAP
                self.scoreMatrix[i][j] = max(diag, left, top)

        self.log("Calculating the Score Matrix:", self.scoreMatrix)

    def optimal_alignment(self):
        self.calculate_score_matrix(len(self.seq1), len(self.seq2))

        align1 = ""
        align2 = ""
        i, j = len(self.seq1), len(self.seq2)
         
        def backtracking(i, j, align1, align2):
            if not (i > 0 or j > 0):
                self.seq1, self.seq2 = align1[::-1], align2[::-1]
                return 
            self.seqScore += self.score(i, j)
            score_current = self.scoreMatrix[i][j]
            score_diagonal = self.scoreMatrix[i - 1][j - 1]
            score_left = self.scoreMatrix[i][j - 1]
            if i > 0 and j > 0 and score_current == score_diagonal + self.score(i, j):
                return backtracking(
                    i - 1,
                    j - 1, 
                    align1 + self.seq1[i - 1], 
                    align2 + self.seq2[j - 1]
                    )
            elif i > 0 and score_current == score_left + GAP:
                return backtracking(
                    i - 1, 
                    j, 
                    align1 + self.seq1[i - 1], 
                    align2 + "-"
                )
            else:
                return backtracking(
                    i, 
                    j - 1, 
                    align1 + "-", 
                    align2 + self.seq2[j - 1]
                )

        return backtracking(i, j, align1, align2)
    
    def score(self, i, j):
        return MATCH if self.seq1[i - 1] == self.seq2[j - 1] else MISMATCH
    
    def log(self, message, matrix=None):
        if not ScoreMatrix.VERBOSE: 
            return
        if matrix is None:
            h.log(message)
            return
        rows = [""] + list(self.seq1)
        columns = [""] + list(self.seq2)
        df = pd.DataFrame(matrix.astype(int), rows, columns)
        h.log(message)
        h.log(df.to_string())
        h.log("\n")
