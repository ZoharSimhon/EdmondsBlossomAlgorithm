# Blossom-Edmond Algorithm

This repository contains a Python implementation of the Blossom-Edmond algorithm, a graph algorithm used for finding maximum weighted matching in general graphs.

## Overview
The Blossom-Edmond algorithm is a graph algorithm used for finding the maximum matching in general graphs. It is an extension of Edmonds' algorithm, which was initially designed for finding maximum cardinality matching in bipartite graphs.

The algorithm employs a combination of augmenting paths and blossom contractions to iteratively improve the matching. Here's a step-by-step explanation of the Blossom-Edmond algorithm:

1. **Initialization**: Start with an empty matching M.

2. **Find an augmenting path**: An augmenting path is a path that starts and ends at unmatched vertices and alternates between matched and unmatched edges. The algorithm searches for an augmenting path using breadth-first search (BFS)  starting from unmatched vertices. If an augmenting path is found, proceed to step 3. Otherwise, the current matching M is a maximum matching, and the algorithm terminates.

3. **Augment the matching**: Given an augmenting path, the algorithm updates the matching M by flipping the matched and unmatched edges along the path. This operation increases the size of the matching by one.

4. **Handle blossoms**: A blossom is a subgraph formed by an odd cycle of alternating matched and unmatched edges. When an augmenting path reaches a node inside a blossom, the algorithm contracts the blossom into a single super node. This contraction reduces the graph size and simplifies subsequent searches for augmenting paths.

5. **Repeat steps 2-4**: After augmenting the matching or contracting a blossom, the algorithm repeats steps 2-4 until no more augmenting paths can be found.

6. **Output**: The algorithm outputs the final matching, which is a maximum matching in the given graph.

The time complexity of the Blossom-Edmond algorithm is O(n^4), where n is the number of vertices in the graph. However, in practice, it often performs much faster due to various optimizations and data structures used to speed up the computations.

The algorithm has various applications, including in matching problems, network flow optimization, and combinatorial optimization.

For a more detailed understanding of the Blossom-Edmond algorithm, you can refer to the **references** section

## Usage

To use the Blossom-Edmond algorithm, follow these steps:

1. Install Python (version 3.6 or above) on your system if you haven't already.

1. Clone this repository to your local machine or download the source code.

1. Open a terminal or command prompt and navigate to the directory where you cloned/downloaded the repository.

1. Install the required dependencies by running the following command:
    ```
    pip install networkx
    pip install matplotlib
    ```

1. Uncomment the desired example or create your own example by creating a list of nodes and a list of tuples representing the edges

1. Run the command
    ```
    python3 main.py
    ```
1. view the algorithm in action

## Acknowledgments

The Blossom-Edmond algorithm implementation in this repository is based on the original work by Jack Edmonds and other contributors. Their contributions to the field of graph theory are greatly appreciated.

## References

If you are interested in learning more about the Blossom-Edmond algorithm and its underlying concepts, you may find the following resources helpful:

- The Blossom algorithm by Tomáš Sláma https://www.youtube.com/watch?v=3roPs1Bvg1Q
- Edmonds, J. (1965). Paths, trees, and flowers. *Canadian Journal of Mathematics*, 17(3), 449-467.
- Harold N. Gabow's lecture notes on [Matching and Matroids](http://www.cs.colorado.edu/~hal/ga77/notes.pdf).
- Wikipedia page on [Blossom algorithm](https://en.wikipedia.org/wiki/Blossom_algorithm).

---