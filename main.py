from Algo import createGraph, showGraph, findMaximumMatching


nodesNX = [i for i in range(8)]
# edgesNX = [(0, 1), (1, 2), (3, 2), (4, 3), (4, 5)]  # no blossoms
# edgesNX = [(0, 1), (1, 2), (0, 2), (3, 2), (4, 3)]  # one blossom
# edgesNX = [(0, 1), (1, 2), (3, 2), (3, 0), (4, 5), (3, 4)]  # no blossom
edgesNX = [(0, 1), (1, 2), (3, 2), (3, 4), (4, 5), (0, 4),(5,6),(2,7)]  # 5-cycle
# edgesNX = [(0, 1), (0, 2), (1, 2), (2, 4), (3, 2), (4, 3), (4, 5)]

G = createGraph(nodesNX, edgesNX)
findMaximumMatching(G)
showGraph(G)
