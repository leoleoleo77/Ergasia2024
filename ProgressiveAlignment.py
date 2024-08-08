import ScoreMatrix as sm
import SequenceGenerator as sg
import pandas as pd
import Helper as h


data = sg.SequenceGenerator()

# 1. Using standard pairwise alignment, calculate a matrix of distances (alignment scores) between each pair of sequences. 
#    Consider this as an N-clique G, where edge {i,j} is labeled with the score of an optimal alignment of the i-th and j-th sequences.+

n = len(data.datasetA) # n = 15
alignmentScores = {}

for i in range(n):
    for j in range(i + 1, n):
        score = sm.ScoreMatrix(data.datasetA[i], data.datasetA[j]).seqScore
        alignmentScores.update({tuple((i, j)): score})

h.log("The matrix of distances (alignment scores) between each pair of sequences:")
for pair in alignmentScores:
    h.log(f"{str(pair)}: {alignmentScores[pair]}")


# 2. Use Kruskal's algorithm to find a minimum spanning tree of G. 
#    Whenever a minimum spanning tree edge would connect two components, 
#    instead add a new root node with directed edges to the roots of the two components. This is the "guide tree".

# This line sorts the dictionary based on the value 
# I honestly have no idea how it works, source: https://t.ly/ldTKM
alignmentScores = dict(sorted(
    alignmentScores.items(), 
    key=lambda item: item[1], 
    reverse=True))
h.log(str(alignmentScores)) 

for pair in alignmentScores:
    h.log(f"{str(pair)}: {alignmentScores[pair]}")
