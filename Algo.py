import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


def createGraph(nodesNX, edgesNX):
    # add all the nodes to unmatched nodes list
    G = nx.Graph(unmatchedNodes=nodesNX, superNodes=[])
    G.add_nodes_from(nodesNX)
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


# def findFreeNode(G):
#     for node in G.nodes:
#         if G.nodes[node]['free']:
#             return node
#     return -1


def find_ancestors(G, node):
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


def shrinkBlossom(G, blossom):
    superNode = nx.Graph(original=[])
    G.add_node(superNode)
    G.graph['superNodes'].append(superNode)

    superNode.add_node(blossom[0], parent=G.nodes[blossom[0]]['parent'],
                       visited=G.nodes[blossom[0]]['visited'], neighbors=[blossom[-1]])
    for i in range(1, len(blossom)):
        superNode.add_node(blossom[i], parent=G.nodes[blossom[i]]['parent'],
                           visited=G.nodes[blossom[i]]['visited'], neighbors=[blossom[i-1]])
        superNode.add_edge((blossom[i-1], blossom[i]))
    superNode.add_edge((blossom[-1], blossom[0]))

    for node in blossom:
        for neighbor in G.neighbors(node):
            if neighbor not in blossom:
                superNode.graph['original'].append((node, neighbor))
                G.add_edge((superNode, neighbor))
                superNode.nodes[node]['neighbors'].append(neighbor)
                if G.nodes[neighbor]['parent'] in blossom:
                    G.nodes[neighbor]['parent'] = superNode

    G.remove_nodes_from(blossom)

    return superNode


def expandSupernode(G, superNode):
    for node in superNode.nodes:
        G.add_node(node, parent=G.nodes[node]['parent'],
                   visited=G.nodes[node]['visited'])
    for node in superNode.nodes:
        for neighbor in superNode.nodes[node]['neighbors']:
            G.add_edge((node, neighbor))

    G.remove_node(superNode)


def replacePath(G, path, superNode, cycle):
    index = path.index(superNode)
    nodes = path[:index]
    cur_node = nodes[-1]
    for edge in superNode.graph['original']:
        if edge[0] == cur_node:
            cur_node = edge[1]
            break
        if edge[1] == cur_node:
            cur_node = edge[0]
            break
    while G.nodes[cur_node]['parent'] != superNode.graph['parent']:
        nodes.append(cur_node)
        nodes.append(G.nodes[cur_node]['mate'])
        neighbor = G.nodes[cur_node]['matchedWith']
        for node in G.neighbors(neighbor):
            if node != cur_node and node in cycle:
                cur_node = node
                break
        # else:
            # raise Exception("replace error.")
    nodes.append(cur_node)
    path = nodes + path[index+1:]


def constructAugmentingPath(G, node, cycle):
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
        replacePath(G, path, superNode, cycle)

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
    while q:
        current = q.popleft()
        G.nodes[current]['visited'] = True
        for node in G.neighbors(current):
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
                    superNode.graph['parent'] = G.nodes[node]['parent']
                    superNode.graph['matchedWith'] = G.nodes[node]['matchedWith']
                    q.appendleft(superNode)
                    break

            elif G.nodes[node]['matchedWith'] == None:
                G.nodes[node]['parent'] = current
                return constructAugmentingPath(G, node, cycle)

    print(q)

def invertPath(G, path):
    for i in range(0, len(path), 2):
        G.nodes[path[i]]['matchedWith'] = path[i+1]
        G.nodes[path[i+1]]['matchedWith'] = path[i]

def findMaximumMatching(G):
    while G.graph['unmatchedNodes']:
        for unmatchedNode in G.graph['unmatchedNodes']:
            path = findAugmentingPath(G, unmatchedNode)
            invertPath(G, path)
            G.graph['unmatchedNodes'].remove(path[0])
            G.graph['unmatchedNodes'].remove(path[-1])
            break
        # G.graph['unmatchedNodes'].remove()
