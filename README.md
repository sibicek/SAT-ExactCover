# SAT-ExactCover
## Problem Definition
A collection of subsets  
\( S = \{ S_1, \dots, S_m \} \)  
over a set  
\( X = \{ 1, \dots, n \} \)

**Decision question:**  
Is there a subcollection \( S^* \subseteq S \) such that each element in \( X \) is contained in exactly one subset in \( S^* \)?  
In other words, does \( S^* \) form an **exact cover** of \( X \) — a partition of \( X \) consisting of subsets from \( S \)?

**Decision output:**  
`SAT` if such a selection exists; `UNSAT` otherwise.

**Input format** 
n m
S1
S2
S3
...
Sm

n - number of elements in set X
m - number of subsets in the collection of subsets S
Si - integers representing the elements of subset Si

**Valid input examples**
4 3
1 2
2 3
3 4
Decision output: UNSAT

3 3
1
2 
3 
Decision output: SAT

