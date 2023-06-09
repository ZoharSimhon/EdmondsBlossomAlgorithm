# import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import numpy as np


def createGraph(nodesNX, edgesNX):
    # add all the nodes to unmatched nodes list
    G = nx.Graph(unmatchedNodes=nodesNX, superNodes=[])
    G.add_nodes_from(nodesNX, matchedWith=None, parent=None)
    G.add_edges_from(edgesNX)
    return G


def showGraph(G):
    # random.seed(100)
    np.random.seed(100)
    # define an array of the edges colors
    # edge_colors = [G.edges[edge]['color'] for edge in G.edges]

    # define an array of the vertices colors - decide the color in accordance to whether the node is matched or not
    # node_colors = ['lightcoral' if G.nodes[node]
    #    ['isMatched'] else 'lightblue' for node in G.nodes]

    # drawing the graph
    node_colors = ["lightblue" if node in G.graph['unmatchedNodes'] else "lightcoral" for node in G.nodes]
    edge_colors = ["lightcoral" if G.nodes[u]['matchedWith']==v and G.nodes[v]['matchedWith']==u else "lightblue" for (u,v) in G.edges ]
    node_colors[list(G.nodes).index(G.graph['current'])] = "limegreen"
    node_colors[G.graph['checked']] = "crimson"
    plt.clf()
    nx.draw_networkx(G, node_color=node_colors,
                    edge_color=edge_colors, with_labels=True)
    # nx.draw(G)
    # setting the plot to non-blocking so we can update the graph with the algorithm
    plt.ion()
    # show the graph in a pop-up window
    plt.show()

    # wait before continuing to the next iteration
    plt.pause(2)


# def findFreeNode(G):
#     for node in G.nodes:
#         if G.nodes[node]['free']:
#             return node
#     return -1


def findAncestors(G, node):
    ancestors = [node]
    while G.nodes[node]['parent'] != None:
        node = G.nodes[node]['parent']
        ancestors.append(node)
    return ancestors


def findCycle(G, node1, node2):
    ancestors1 = findAncestors(G, node1)
    ancestors2 = findAncestors(G, node2)
    i = len(ancestors1) - 1
    j = len(ancestors2) - 1
    while ancestors1[i] == ancestors2[j]:
        i -= 1
        j -= 1

    cycle = ancestors1[:i+1] + ancestors2[j+1::-1]
    return cycle


def shrinkBlossom(G, blossom):
    superNodeName = "s" + str(len(G.graph['superNodes']))
    G.add_node(superNodeName,original=[],sub=[],parent=None)
    G.graph['superNodes'].append(superNodeName)

    # superNode.add_node(blossom[0], parent=G.nodes[blossom[0]]['parent'],
    #                    visited=G.nodes[blossom[0]]['visited'], neighbors=[blossom[-1]])
    # for i in range(1, len(blossom)):
    #     superNode.add_node(blossom[i], parent=G.nodes[blossom[i]]['parent'],
    #                        visited=G.nodes[blossom[i]]['visited'], neighbors=[blossom[i-1]])
    #     superNode.add_edge(blossom[i-1], blossom[i])
    # superNode.add_edge(blossom[-1], blossom[0])

    for node in blossom:
        G.nodes[superNodeName]['sub'].append(node)
        for neighbor in G.neighbors(node):
            if neighbor not in blossom:
                G.nodes[superNodeName]['original'].append((node, neighbor))
                if G.nodes[neighbor]['parent'] in blossom:
                    G.nodes[neighbor]['parent'] = superNodeName

        for (node1, node2) in G.nodes[superNodeName]['original']:
            G.remove_edge(node1,node2)
            G.add_edge(superNodeName, node2)

    return superNodeName


def expandSupernode(G, superNodeName):
    for (node1, node2) in G.nodes[superNodeName]['original']:
        G.add_edge(node1,node2)
        G.remove_edge(superNodeName,node2)
    # showGraph(G)
    # for node in superNode.nodes:
    #     G.add_node(node, parent=G.nodes[node]['parent'],
    #                visited=G.nodes[node]['visited'])
    # for node in superNode.nodes:
    #     for neighbor in superNode.nodes[node]['neighbors']:
    #         G.add_edge(node, neighbor)

    # G.remove_node(superNode)


def replacePath(G, path, superNode):
    index = path.index(superNode)
    nodes = path[:index]
    cur_node = nodes[-1]
    for edge in G.nodes[superNode]['original']:
        if edge[0] == cur_node:
            cur_node = edge[1]
            break
        if edge[1] == cur_node:
            cur_node = edge[0]
            break
    while G.nodes[cur_node]['parent'] != G.nodes[superNode]['parent']:
        nodes.append(cur_node)
        m = G.nodes[cur_node]['matchedWith']
        nodes.append(m)
        for node in G.neighbors(m):
            if node != cur_node and node in G.nodes[superNode]['sub']:
                cur_node = node
                break
        # else:
            # raise Exception("replace error.")
    nodes.append(cur_node)
    path = nodes + path[index+1:]
    return path


def constructAugmentingPath(G, node):
    path = []
    path.append(node)
    node = G.nodes[node]['parent']
    path.append(node)
    while G.nodes[node]['matchedWith']:
        node = G.nodes[node]['parent']
        path.append(node)

    while G.graph['superNodes']:
        superNode = G.graph['superNodes'].pop()
        expandSupernode(G, superNode)
        print("before: ",path)
        path = replacePath(G, path, superNode)
        print("after: ",path)

    while G.nodes[path[0]]['matchedWith']:
        path.insert(G.nodes[path[0]]['parent'], 0)

    while G.nodes[path[-1]]['matchedWith']:
        path.append(G.nodes[path[-1]]['parent'])

    return path


def findAugmentingPath(G, root):
    for node in G.nodes:
        G.nodes[node]['visited'] = False
        G.nodes[node]['parent'] = None
    q = deque()
    q.append(root)
    print("root: ",root)
    while q:
        current = q.popleft()
        G.graph['current'] = current
        G.nodes[current]['visited'] = True
        for node in G.neighbors(current):
            G.graph['checked'] = node
            showGraph(G)
            if node == G.nodes[current]['parent']:
                continue
            
            elif G.nodes[node]['visited']:
                cycle = findCycle(G, node, current)
                if len(cycle) % 2 == 1:
                    superNode = shrinkBlossom(G, cycle)
                    for v in cycle:
                        if v in q:
                            q.remove(v)
                    G.nodes[superNode]['visited'] = True
                    while G.nodes[node]['parent'] in cycle:
                        node = G.nodes[node]['parent']
                    G.nodes[superNode]['parent'] = G.nodes[node]['parent']
                    G.nodes[superNode]['matchedWith'] = G.nodes[node]['matchedWith']
                    q.appendleft(superNode)
                    break

            elif G.nodes[node]['matchedWith'] == None:
                G.nodes[node]['parent'] = current
                return constructAugmentingPath(G, node)
            
            elif G.nodes[node]['matchedWith'] != current:
                    G.nodes[node]['visited'] = True
                    G.nodes[G.nodes[node]['matchedWith']]['visited'] = True
                    G.nodes[node]['parent'] = current
                    G.nodes[G.nodes[node]['matchedWith']]['parent'] = node
                    q.append(G.nodes[node]['matchedWith'])

        if not q:
            raise Exception('cannot find an augmenting path')

def invertPath(G, path):
    print(path)
    for i in range(0, len(path), 2):
        G.nodes[path[i]]['matchedWith'] = path[i+1]
        G.nodes[path[i+1]]['matchedWith'] = path[i]

def findMaximumMatching(G):
    while G.graph['unmatchedNodes']:
        for unmatchedNode in G.graph['unmatchedNodes']:
            try:
                path = findAugmentingPath(G, unmatchedNode)
                invertPath(G, path)
                G.graph['unmatchedNodes'].remove(path[0])
                G.graph['unmatchedNodes'].remove(path[-1])
                break
            except Exception as e:
                print(e)
                return
        showGraph(G)
        # G.graph['unmatchedNodes'].remove()
