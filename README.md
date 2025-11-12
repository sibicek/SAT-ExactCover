# SAT-ExactCover
## Problem Definition
Let $X = \{1, 2, \dots, n\}$ and $S = \{S_1, S_2, \dots, S_m\}$ be a collection of subsets of $X$.

**Decision question:**  
Is there a subcollection $S^* \subseteq S$ such that each element in $X$ appears in exactly one subset of S*?  
Equivalently, does S* form an exact cover of $X$?

**Decision output:**  
- SAT if such a selection exists.  
- UNSAT otherwise.

**Input format** 
```
n m
S1
S2
S3
...
Sm

n - number of elements in set X
m - number of subsets in the collection of subsets S
Si - integers representing the elements of subset Si
```
**Example 1 (UNSAT):**
```
4 3
1 2
2 3
3 4
```
Decision output: UNSAT

**Example 2 (SAT):**
```
3 3
1
2 
3
```
Decision output: SAT

## Encoding

The problem is encoded using variables $s_i$ that indicate whether we select the subset $S_i$.  

For each element $x \in X$, define  

$$
I(x) = \{ i \mid x \in S_i \}
$$

We require that each element $x \in X$ is covered exactly once:

1. **At least one subset covers x**:  
$$
\bigvee_{j \in I(x)} s_j
$$

3. **At most one subset covers x**:  
$$
\neg s_j \vee \neg s_k \quad \text{for all } j \neq k \text{ in } I(x)
$$
