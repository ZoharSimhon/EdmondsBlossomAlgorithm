from maxMatchingAlgorithm import createGraph, showGraph, findMaximumMatching
from minimumLineCover import findMinimumLineCover

# no cycle
# nodes = [i for i in range(6)]
# edges = [(0, 1), (1, 2), (3, 2), (4, 3), (4, 5)]
  
# nodes = [i for i in range(5)]
# edges = [(0, 1), (1, 2), (0, 2), (3, 2), (4, 3)]  # 3-cycle - not perfect matching

nodes = [i for i in range(9)]
edges = [(0,5),(1,5),(1,7),(2,6),(2,7),(2,8),(3,7),(4,8)]  # bipatite graph - not perfect matching

# nodes = [i for i in range(8)]
# edges = [(0, 1), (1, 2), (3, 2), (3, 4), (4, 5), (0, 4),(5,6),(2,7)]  # 5-cycle

# nodes = [i for i in range(6)]
# edges = [(0, 1), (0, 2), (1, 2), (2, 4), (3, 2), (4, 3), (4, 5)] # double 3-cycle

# nodes = [i for i in range(6)]
# edges = [(0, 1), (1, 2), (0, 2), (3, 2), (4, 3), (4,5)]  # 3-cycle

G = createGraph(nodes, edges)
findMaximumMatching(G)
showGraph(G)

findMinimumLineCover(G)
