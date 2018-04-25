import numpy as np
import networkx as nx


def paris(graph):
    """
     Given a graph, compute the paris hierarchy.

     Parameters
     ----------
     dendrogram: networkx.graph
         A graph with weighted edges.

     Returns
     -------
     dendrogram: numpy.array
         The paris hierachical clustering is represneted by the dendrogram. Each line of the dendrogram contains the
         merged nodes, the distance between merged nodes and the number of nodes in the new cluster.

     References
     ----------
     -
     """
    graph_copy = graph.copy()
    nodes = list(graph_copy.nodes())
    n_nodes = len(nodes)
    graph_copy = nx.convert_node_labels_to_integers(graph_copy)

    w = {u: 0 for u in range(n_nodes)}
    wtot = 0
    for (u, v) in graph_copy.edges():
        weight = graph_copy[u][v]['weight']
        w[u] += weight
        w[v] += weight
        wtot += 2 * weight
    s = {u: 1 for u in range(n_nodes)}
    cc = []
    dendrogram = []
    u = n_nodes

    while n_nodes > 0:
        chain = [list(graph_copy.nodes())[0]]
        while chain != []:
            a = chain.pop()
            d_min = float("inf")
            b = -1
            neighbors_a = list(graph_copy.neighbors(a))
            for v in neighbors_a:
                if v != a:
                    d = w[v] * w[a] / float(graph_copy[a][v]['weight']) / float(wtot)
                    if d < d_min:
                        b = v
                        d_min = d
                    elif d == d_min:
                        b = min(b, v)
            d = d_min
            if chain != []:
                c = chain.pop()
                if b == c:
                    dendrogram.append([a, b, d, s[a] + s[b]])
                    graph_copy.add_node(u)
                    neighbors_a = list(graph_copy.neighbors(a))
                    neighbors_b = list(graph_copy.neighbors(b))
                    for v in neighbors_a:
                        graph_copy.add_edge(u, v, weight=graph_copy[a][v]['weight'])
                    for v in neighbors_b:
                        if graph_copy.has_edge(u, v):
                            graph_copy[u][v]['weight'] += graph_copy[b][v]['weight']
                        else:
                            graph_copy.add_edge(u, v, weight=graph_copy[b][v]['weight'])
                    graph_copy.remove_node(a)
                    graph_copy.remove_node(b)
                    n_nodes -= 1
                    w[u] = w.pop(a) + w.pop(b)
                    s[u] = s.pop(a) + s.pop(b)
                    u += 1
                else:
                    chain.append(c)
                    chain.append(a)
                    chain.append(b)
            elif b >= 0:
                chain.append(a)
                chain.append(b)
            else:
                cc.append((a, s[a]))
                graph_copy.remove_node(a)
                w.pop(a)
                s.pop(a)
                n_nodes -= 1

    a, s = cc.pop()
    for b, t in cc:
        s += t
        dendrogram.append([a, b, float("inf"), s])
        a = u
        u += 1

    return reorder_dendrogram(np.array(dendrogram))


def reorder_dendrogram(dendrogram):
    """
     Given a graph, compute the paris hierarchy

     Parameters
     ----------
     dendrogram: numpy.array
         Each line of the dendrogram contains the merged nodes, the distance between merged nodes and the number of
         nodes in the new cluster. The lines are not sorted with respect to increasing distances.

     Returns
     -------
     dendrogram: numpy.array
         Each line of the dendrogram contains the merged nodes, the distance between merged nodes and the number of
         nodes in the new cluster. The lines are sorted with respect to increasing distances.

     References
     ----------
     -
     """
    n = np.shape(dendrogram)[0] + 1
    order = np.zeros((2, n - 1), float)
    order[0] = range(n - 1)
    order[1] = np.array(dendrogram)[:, 2]
    index = np.lexsort(order)
    n_index = {i: i for i in range(n)}
    n_index.update({n + index[t]: n + t for t in range(n - 1)})
    return np.array([[n_index[int(dendrogram[t][0])], n_index[int(dendrogram[t][1])], dendrogram[t][2], dendrogram[t][3]] for t in range(n - 1)])[index, :]
