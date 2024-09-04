import ScoreMatrix as sm
import SequenceGenerator as sg
import pandas as pd
import Helper as h
import GuideTree as gt


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

MST = [] # Minimum Spanning Tree
edges = 0

for pair in alignmentScores:

    if len(MST) == 0:
        h.log(f"{str(pair)}: {alignmentScores[pair]} - Adding it to the MST")
        MST.append(pair)
        edges += 1
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
        h.log(f"{str(pair)}: {alignmentScores[pair]} - Adding it to the MST")
        MST.append(pair)
        edges += 1
        if edges == n - 1:
            break
    else:
        h.log(f"{str(pair)}: {alignmentScores[pair]} Cycle created by it, skipping")

h.log("The minimum spanning tree:")
h.log(str(MST))

guideTree = gt.GuideTree().construct(MST)
h.log(guideTree.info())

# 3. Do pairwise alignments according to the guide tree, working from the leaves to the root. 
#    A node u with children v and w corresponds to an alignment of the leaves of v's subtree (already aligned inductively) 
#    with the leaves of w's subtree (already aligned).
#
# Details of pairwise alignment
#   Suppose V is an alignment of the sequences at the leaves of v's subtree, 
#   and W is an alignment of the sequences at the leaves of w's subtree. 
#   Let {a,b} be the pair of sequences that caused these subtrees to be merged, and let A be the optimal alignment of a and b. 
#   Use A to guide the alignment of the two alignments V and W.

def pairwise_alignment(tree):
    for node in tree.nodes:
        if not node.is_root(): continue
        node.seq = iterate_tree(node)
    print(tree.info())
    

def iterate_tree(root):
    if not root.has_children():
        return data.datasetA[root.i]
    for child in root.children:
        child.seq = iterate_tree(child)
    return sequence_alignment(root)

def sequence_alignment(root):
    # Let {a,b} be the pair of sequences that caused these subtrees to be merged
    rootOrigins = root.createdBy 
    # and let A be the optimal alignment of a and b. 
    optimalAlignment = sm.ScoreMatrix(rootOrigins[0].seq, rootOrigins[1].seq).alignedSequences()
    rootOrigins[0].seq, rootOrigins[1].seq = optimalAlignment
    for i in range(1):
        for seq in [root.children[i].seq]:
            if seq != rootOrigins[i].seq:
                print("hi")
                seq = sm.ScoreMatrix(seq, rootOrigins[i].seq).alignedSequences()

    return optimalAlignment

        


pairwise_alignment(guideTree)


