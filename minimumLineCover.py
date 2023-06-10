import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def showGraph(G):
    nodes = []
    for node in G.nodes:
        if G.nodes[node]['visible']:
            nodes.append(node)
    edges = []
    for (u,v) in G.edges:
        if G.nodes[u]['visible'] and G.nodes[v]['visible']:
            edges.append((u,v))
            
    subgraph = G.subgraph(nodes)
    np.random.seed(100)
    node_colors = ["indianred" if node in G.graph['unmatchedNodes'] else "lightcoral" for node in nodes]
    
    edge_colors = []
    ["lightcoral" if G.nodes[u]['matchedWith']==v and G.nodes[v]['matchedWith']==u else "lightblue" for (u,v) in edges ]
    for (u,v) in edges:
        if 'color' in G.edges[(u,v)]:
            edge_colors.append(G.edges[(u,v)]['color'])
        
        elif G.nodes[u]['matchedWith']==v and G.nodes[v]['matchedWith']==u:
           edge_colors.append("lightcoral") 
        
        else:
           edge_colors.append("lightblue") 
    
    plt.clf()
    nx.draw_networkx(subgraph, node_color=node_colors,
                    edge_color=edge_colors, with_labels=True)
    plt.ion()
    plt.show()
    plt.pause(1.5)


def findMinimumLineCover(G):
    # define the vertices without matching (V(G)-V(M))
    U = []
    for node in G.graph['unmatchedNodes'] :
        if G.nodes[node]['visible']:
            U.append(node)
            
    print("U:", U)

    # define the connecting edges between U to V(M)
    S = []
    for u in U:
        neighbors = list(G.neighbors(u))
        for neighbor in neighbors:
            if G.nodes[neighbor]['matchedWith']:
                S.append((u,neighbor))
                #print the edge (u,neighbor)
                G.edges[(u,neighbor)]['color'] = "indianred"
                showGraph(G)
                break
    print ("S:", S)
    showGraph(G)
    
    #find the number of nodes and he number of vertices in the matching
    nodesCounter = 0
    matchingCounter = 0
    for node in G.nodes:
        if G.nodes[node]['visible']:
            if G.nodes[node]['matchedWith'] != None:
                matchingCounter +=1
            nodesCounter += 1
            
    print("The number of nodes in G is:", nodesCounter)
    print("The number of edges in M is:", matchingCounter//2)
    print("The number of edges in L is:", matchingCounter//2 + len(S))
    
       


   