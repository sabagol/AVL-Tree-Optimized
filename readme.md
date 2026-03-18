# Optimized AVL Tree Implementation with Finger Search

## Project Overview

This project implements a robust, self-balancing AVL Tree in Python. Beyond standard dictionary operations, it features advanced algorithmic optimizations like Finger Search and Finger Insert, which leverage spatial locality to achieve faster-than-logarithmic performance for specific insertion sequences.

The implementation was rigorously analyzed through a series of experiments comparing theoretical complexity bounds against empirical performance across various data distributions (sorted, reversed, random, and near-sorted).

## Key Features

* **Self-Balancing Logic:** Complete implementation of rotations (LL, LR, RR, RL) and height-based rebalancing during insertion and deletion.

* **Finger Search & Insert:** Optimized traversal starting from the maximum node, reducing the search path to $O(\log d)$ where $d$ is the distance between the finger and the target key.

* **Complex Tree Operations:** Full support for Join and Split operations, maintaining AVL properties with $O(\log n)$ complexity.

* **Empirical Analysis:** Conducted depth-first analysis on cost-of-balance, proving amortized $O(1)$ rebalancing costs in practice.

# Technical Highlights

* **Mathematical Proofs:** Validated the $O(n \log(\frac{I}{n} + 2))$ time complexity for finger-based sequences using the AM-GM inequality.

* **Object-Oriented Design:** Clean separation between AVLNode and AVLTree classes with a focus on modularity and clear parent-child pointer management.

# File Structure

```AVLTree.py```: The core implementation containing the AVL logic and finger-based optimizations.

```experiments_and_documentation.pdf```: A detailed research report featuring empirical data, complexity proofs, and method descriptions.

## Performance Summary

| Array Type | Theoretical Bound | Experimental Result
|---|---|---|
| Sorted | $O(n)$ | Matches Amortized $O(1)$ per op |
| Random | $O(n \log n)$ | Within Predicted Bounds |

## Author

Saba Golbandi