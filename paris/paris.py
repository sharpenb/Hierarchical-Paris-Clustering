import numpy as np
import networkx as nx


def paris(graph):
    graph_copy = graph.copy()
    nodes = list(graph_copy.nodes())
    n_nodes = len(nodes)

    # index nodes from 0 to n - 1
    graph_copy = nx.convert_node_labels_to_integers(graph_copy)

    # node weights
    w = {u: 0 for u in range(n_nodes)}
    wtot = 0
    for (u, v) in graph_copy.edges():
        weight = graph_copy[u][v]['weight']
        w[u] += weight
        w[v] += weight
        wtot += 2 * weight

    # cluster sizes
    s = {u: 1 for u in range(n_nodes)}

    # connected components
    cc = []

    # dendrogram as list of merges
    D = []

    # cluster index
    u = n_nodes
    while n_nodes > 0:
        # nearest-neighbor chain
        chain = [list(graph_copy.nodes())[0]]
        while chain != []:
            a = chain.pop()
            # nearest neighbor
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
                    # merge a,b
                    D.append([a, b, d, s[a] + s[b]])
                    # update graph
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
                    # update weight and size
                    w[u] = w.pop(a) + w.pop(b)
                    s[u] = s.pop(a) + s.pop(b)
                    # change cluster index
                    u += 1
                else:
                    chain.append(c)
                    chain.append(a)
                    chain.append(b)
            elif b >= 0:
                chain.append(a)
                chain.append(b)
            else:
                # remove the connected component
                cc.append((a, s[a]))
                graph_copy.remove_node(a)
                w.pop(a)
                s.pop(a)
                n_nodes -= 1

    # add connected components to the dendrogram
    a, s = cc.pop()
    for b, t in cc:
        s += t
        D.append([a, b, float("inf"), s])
        a = u
        u += 1

    return reorder_dendrogram(np.array(D))


def reorder_dendrogram(D):
    n = np.shape(D)[0] + 1
    order = np.zeros((2, n - 1), float)
    order[0] = range(n - 1)
    order[1] = np.array(D)[:, 2]
    index = np.lexsort(order)
    nindex = {i: i for i in range(n)}
    nindex.update({n + index[t]: n + t for t in range(n - 1)})
    return np.array([[nindex[int(D[t][0])], nindex[int(D[t][1])], D[t][2], D[t][3]] for t in range(n - 1)])[index, :]
