# -*- coding: utf-8 -*-
"""
==================================================
Demo of the Louvain algorithm on the bow tie graph
==================================================
"""
print(__doc__)

import networkx as nx
import cylouvain

# ############################################################################################
# Generate the graph
graph = nx.Graph()
graph.add_nodes_from(['a', 'b', 'c', 'd', 'e'])
graph.add_edges_from([('a', 'b'), ('a', 'c'), ('b', 'c'), ('c', 'd'), ('c', 'e'), ('d', 'e')])

# ############################################################################################
# Louvain on the NetworkX graph
print("Apply the algorithm to the NetworkX Graph object")

partition = cylouvain.best_partition(graph)
modularity = cylouvain.modularity(partition, graph)

print("Output partition:")
print(partition)
print("Modularity %0.3f\n" % modularity)

# #############################################################################
# Plot result
print("Plot the result\n")
import matplotlib.pyplot as plt

plt.figure()
plt.axis('off')
pos = nx.fruchterman_reingold_layout(graph)
nx.draw_networkx_edges(graph, pos)
nx.draw_networkx_nodes(graph, pos, node_color=[partition[node] for node in graph])
plt.show()

# ############################################################################################
# Louvain on the adjacency matrix
print("Apply the algorithm to the adjacency matrix (SciPy CSR matrix)")

adj_matrix = nx.adj_matrix(graph)
partition = cylouvain.best_partition(adj_matrix)
modularity = cylouvain.modularity(partition, adj_matrix)

print("Output partition:")
print(partition)
print("Modularity %0.3f" % modularity)