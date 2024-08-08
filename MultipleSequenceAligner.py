import numpy as np
import SequenceGenerator as sg
import Helper as h

def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-1):

    n, m = len(seq1), len(seq2)
    scoreMatrix = h.calculateScoreMatrix(n, m, seq1, seq2, match, mismatch, gap)
    return h.backtracking(n, m, seq1, seq2, match, mismatch, gap, scoreMatrix)

x = needleman_wunsch("GATTACA", "GCATGCG")
print(x)

# def add_gaps_to_alignment(alignment):
#     max_length = max(len(seq) for seq in alignment)
#     new_alignment = []
#     for seq in alignment:
#         gaps_needed = max_length - len(seq)
#         new_seq = seq + '-' * gaps_needed
#         new_alignment.append(new_seq)
#     return new_alignment

# def progressive_alignment(sequences):
#     aligned_sequences = [sequences[0]]
    
#     for i in range(1, len(sequences)):
#         new_alignment = []
#         for aligned_seq in aligned_sequences:
#             align1, align2 = needleman_wunsch(aligned_seq, sequences[i])
#             new_alignment.append(align1)
#         new_alignment.append(align2)
#         aligned_sequences = add_gaps_to_alignment(new_alignment)
    
#     return aligned_sequences

# aligned = progressive_alignment(sg.StringGenerator().datasetA)
# for i, seq in enumerate(aligned):
#     print(f"Aligned Sequence {i + 1}: {seq} {len(seq)}")
