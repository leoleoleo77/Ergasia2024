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

# 2. Use Kruskal's algorithm to find a minimum spanning tree of G. 
#    Whenever a minimum spanning tree edge would connect two components, 
#    instead add a new root node with directed edges to the roots of the two components. This is the "guide tree".

# Step A of Krukal's algorithm, sort the edges by weight
#   This line sorts the dictionary based on the value 
#   I honestly have no idea how it works, source: https://t.ly/ldTKM
alignmentScores = dict(sorted(
    alignmentScores.items(), 
    key=lambda item: item[1], 
    reverse=True))

h.log("The matrix of distances (alignment scores) between each pair of sequences in order:")
for pair in alignmentScores:
    h.log(f"{str(pair)}: {alignmentScores[pair]}")

MST = [] # Minimum Spanning Tree
nodes = 0

for pair in alignmentScores:
    if len(MST) == 0:
        h.log(f"Adding {pair} to the MST")
        MST.append(pair)
        nodes += 2
        continue
    nodeA, nodeB = pair
    nodeA_in_MST, nodeB_in_MST = (False, False)
    for edge in MST:
        if nodeA in edge:
            nodeA_in_MST = True
        if nodeB in edge:
            nodeB_in_MST = True
    cycleCreated = nodeA_in_MST and nodeB_in_MST
    if not cycleCreated:
        h.log(f"Adding {pair} to the MST")
        MST.append(pair)
        if nodeA_in_MST or nodeB_in_MST:
            nodes += 1
        else:
            nodes += 2
        if nodes == n - 1:
            break
    else:
        h.log(f"Cycle created by {pair}, skipping")

h.log("The minimum spanning tree:")
h.log(str(MST))




