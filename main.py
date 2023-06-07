from algorithm import *
from Algo import *

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

nodesNX = [i for i in range(6)]
edgesNX = [(0, 1), (0, 2), (1, 2), (2, 4), (3, 2), (4, 3), (4, 5)]


nodes = [Node() for i in range(6)]
nodes[0].neighbors.append(nodes[1])
nodes[1].neighbors.append(nodes[0])
nodes[0].neighbors.append(nodes[2])
nodes[2].neighbors.append(nodes[0])
nodes[1].neighbors.append(nodes[2])
nodes[2].neighbors.append(nodes[1])
nodes[2].neighbors.append(nodes[4])
nodes[4].neighbors.append(nodes[2])
nodes[3].neighbors.append(nodes[2])
nodes[2].neighbors.append(nodes[3])
nodes[4].neighbors.append(nodes[3])
nodes[3].neighbors.append(nodes[4])
nodes[4].neighbors.append(nodes[5])
nodes[5].neighbors.append(nodes[4])

# G = createGraph(nodesNX,edgesNX)
# showGraph(G)
# findMaximumMatching(G)

G = nx.Graph()
G.add_nodes_from(nodesNX, free=True)
G.add_edges_from(edgesNX)
K3 = nx.Graph([(0, 1), (1, 2), (2, 0)])
for node in G.nodes:
    K3.add_node(node,free=G.nodes[node]['free'])
# G.add_node(K3.nodes)
for node in K3.nodes:
    print(K3.nodes[node])
# showGraph(G)



# match = Match(nodes)
# match.maximum_matching()

# print(nodes[0].mate)
# print(nodes[1].mate)
# print(nodes[2].mate)
# print(nodes[3].mate)
# print(nodes[4].mate)
# print(nodes[5].mate)
