import ScoreMatrix as sm
import SequenceGenerator as sg
import pandas as pd
import Helper as h


data = sg.SequenceGenerator()

# 1. Using standard pairwise alignment, calculate a matrix of distances (alignment scores) between each pair of sequences. 
#    Consider this as an N-clique G, where edge {i,j} is labeled with the score of an optimal alignment of the i-th and j-th sequences.+

n = len(data.datasetA) # n = 15
matrixOfDistances = [[""] * n for _ in range(n)] # 15x15 matrix

for i in range(n):
    for j in range(i + 1, n):
        alignmentScore = sm.ScoreMatrix(data.datasetA[i], data.datasetA[j]).seqScore
        matrixOfDistances[i][j] = alignmentScore

h.log("The matrix of distances (alignment scores) between each pair of sequences:")
h.log(pd.DataFrame(matrixOfDistances).to_string())


# 2. Use Kruskal's algorithm to find a minimum spanning tree of G. 
#    Whenever a minimum spanning tree edge would connect two components, 
#    instead add a new root node with directed edges to the roots of the two components. This is the "guide tree".


for i in range(n):
    for j in range(i + 1, n):
        matrixOfDistances[j][i] = matrixOfDistances[i][j] # make the matrix symmetric (redundant?s)

