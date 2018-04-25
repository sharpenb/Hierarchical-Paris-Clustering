paris: Hierarchical graph clustering algorithm and dendrogram processing
=========================

paris is a Python module that provides an implementation of the hierarchical clustering algorithm for graphs, paris.
It provides four algorithms able to process dendrograms in order to extract best clusters, clusterings or distances.

Installation
------------

Install the latest version of cylouvain using ``pip`` ::

    $ pip install paris

Dependencies
------------

cylouvain requires:

- Python (>= 2.7 or >= 3.4)
- NumPy
- NetworkX

Simple example
--------------

Build a simple graph with NetworkX::

    >>> import networkx as nx
    >>> graph = nx.Graph()
    >>> graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f'])
    >>> graph.add_edges_from([('a', 'b'), ('a', 'c'), ('b', 'c'),
                              ('c', 'd'),
                              ('d', 'e'), ('d', 'f'), ('f', 'e')])

Compute a partition of the nodes using cylouvain::

    >>> from paris import paris
    >>> dendrogram = paris(graph)

Compute the best clusters, clusterings and distances::

    >>> best_cluster = best_cluster_cut(dendrogram)
    >>> best_homogneous_clustering = best_homogeneous_cut(dendrogram)
    >>> best_heterogneous_clustering = best_heterogeneous_cut(dendrogram)
    >>> best_distance = best_distance

License
-------

Released under the MIT license::

   Copyright (C) 2018 Bertrand Charpentier <bercha@kth.se>
