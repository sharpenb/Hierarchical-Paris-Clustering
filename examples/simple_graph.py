# -*- coding: utf-8 -*-
"""
=============================================
Demo of the Paris algorithm on a simple graph
=============================================
"""
print(__doc__)

from community import best_partition
from python_paris.paris import *
from python_paris.cluster_cut_slicer import *
from python_paris.homogeneous_cut_slicer import *
from python_paris.heterogeneous_cut_slicer import *
from python_paris.distance_slicer import *

# ############################################################################################
# Generate the graph
graph = nx.Graph()
graph.add_nodes_from([0, 1, 2, 3, 4, 5])
graph.add_weighted_edges_from([(0, 1, 1), (0, 2, 1), (1, 2, 1), (2, 3, 1),
                      (3, 4, 1), (3, 5, 1), (4, 5, 1)])

# ############################################################################################
# Apply Paris on the graph
print("Apply the algorithm to the NetworkX Graph object")
dendrogram = paris(graph)

# ############################################################################################
# Process dendrogram
best_cut, best_score = best_cluster_cut(dendrogram)
best_cluster = clustering_from_cluster_cut(dendrogram, best_cut)

best_cut, best_score = best_homogeneous_cut(dendrogram)
best_homogeneous_clustering = clustering_from_homogeneous_cut(dendrogram, best_cut)

best_cut, best_score = best_heterogeneous_cut(dendrogram)
best_heterogeneous_clustering = clustering_from_heterogeneous_cut(dendrogram, best_cut)

best_dist, best_score = best_distance(dendrogram)
best_louvain_clustering = best_partition(graph, resolution=best_dist)

# #############################################################################
# Plot result
print("Plot the result\n")
import matplotlib.pyplot as plt

colors = ['b', 'g', 'r', 'c', 'm', 'y']
pos = nx.fruchterman_reingold_layout(graph)

plt.subplot(2, 2, 1)
plt.title('Best cluster')
plt.axis('off')
nx.draw_networkx_edges(graph, pos)
nodes = nx.draw_networkx_nodes(graph, pos, node_color='k')
nx.draw_networkx_nodes(graph, pos, nodelist=best_cluster, node_color=colors[0])

plt.subplot(2, 2, 2)
plt.title('Best homogeneous clustering')
plt.axis('off')
nx.draw_networkx_edges(graph, pos)
for l in range(min(len(colors), len(best_homogeneous_clustering))):
    nx.draw_networkx_nodes(graph, pos, nodelist=best_homogeneous_clustering[l], node_color=colors[l])

plt.subplot(2, 2, 3)
plt.title('Best heterogeneous clustering')
plt.axis('off')
nx.draw_networkx_edges(graph, pos)
for l in range(min(len(colors), len(best_heterogeneous_clustering))):
    nx.draw_networkx_nodes(graph, pos, nodelist=best_heterogeneous_clustering[l], node_color=colors[l])

plt.subplot(2, 2, 4)
plt.title('Best distance')
plt.axis('off')
nx.draw_networkx_edges(graph, pos)
nx.draw_networkx_nodes(graph, pos, node_color=[colors[best_louvain_clustering[node]] for node in graph])
plt.show()
