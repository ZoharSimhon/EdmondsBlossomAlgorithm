import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


def createGraph(nodesNX, edgesNX):
    G = nx.Graph()
    G.add_nodes_from(nodesNX, free=True)
    G.add_edges_from(edgesNX)
    return G


def showGraph(G):
    # define an array of the edges colors
    # edge_colors = [G.edges[edge]['color'] for edge in G.edges]

    # define an array of the vertices colors - decide the color in accordance to whether the node is matched or not
    # node_colors = ['lightcoral' if G.nodes[node]
             #    ['isMatched'] else 'lightblue' for node in G.nodes]

    # drawing the graph
    # nx.draw_networkx(G, with_labels=True,
                 #  node_color=node_colors, edge_color=edge_colors, arrows=True)
    nx.draw(G)
    # setting the plot to non-blocking so we can update the graph with the algorithm
    # plt.ion()

    # show the graph in a pop-up window
    plt.show()

    # wait before continuing to the next iteration
    # plt.pause(2)


def findFreeNode(G):
    for node in G.nodes:
        if G.nodes[node]['free']:
            return node
    return -1

def find_ancestors(G,node):
    ancestors = [node]
    while G.nodes[node]['parent'] != None:
        node = G.nodes[node]['parent'] 
        ancestors.append(node)
    return ancestors


def findCycle(G, node1, node2):
    ancestors1 = find_ancestors(G, node1)
    ancestors2 = find_ancestors(G, node2)
    i = len(ancestors1) - 1
    j = len(ancestors2) - 1
    while ancestors1[i] == ancestors2[j]:
        i -= 1
        j -= 1

    cycle = ancestors1[:i+1] + ancestors2[j+1::-1]
    return cycle

def shrinkBlossom(G,blossom):
    # G.add_node()
    subnodes = []
    original_edges = []
    for node in blossom:
        subnodes.append(node)
        for neighbor in G.neighbors(node):
            if neighbor not in blossom:
                original_edges.append((node, neighbor))
                if G.nodes[neighbor]['parent'] in blossom:
                    pass
                    # G.nodes[neighbor]['parent']= snode
                    
    # for node1, node2 in snode.original_edges:
    # node1.neighbors.remove(node2)
    # node2.neighbors.remove(node1)
    # node2.neighbors.append(snode)
    # snode.neighbors.append(node2)



def findAugmentingPath(G, root):
    for node in G.nodes:
        G.nodes[node]['visited'] = False
        G.nodes[node]['parent'] = None
    q = deque()
    q.append(root)
    while q:
        current = q.popleft()
        G.nodes[current]['visited'] = True
        for node in G.neighbors(current):
            if node == G.nodes[current]['parent']:
                continue
            elif G.nodes[node]['visited']:
                cycle = findCycle(G, node, current)
                if len(cycle) % 2 == 1:
                    snuperNode = shrinkBlossom(G,cycle)

                
    print(q)


def findMaximumMatching(G):
    while True:
        freeNode = findFreeNode(G)
        print(freeNode)
        if freeNode == -1:
            break
        path = findAugmentingPath(G, freeNode)
        G.nodes[freeNode]['free'] = False
