python-paris: Hierarchical graph clustering algorithm (paris) and dendrogram processing
=========================

The paris package is a Python module that provides an implementation of the hierarchical clustering algorithm for graphs, paris, from the paper:

[Hierarchical Graph Clustering using Node Pair Sampling](https://www.mlgworkshop.org/2018/papers/MLG2018_paper_4.pdf)<br>
Thomas Bonald , Bertrand Charpentier, Alexis Galland, Alexandre Hollocou<br>
Mining and Learning with Graphs (MLG - KDD Workshop), 2018

Additonally, it provides four algorithms able to process dendrograms in order to extract best clusters, clusterings or distances. These algorithms are described in the paper:

[Multi-scale Clustering in Graphs using Modularity](http://www.diva-portal.org/smash/get/diva2:1292782/FULLTEXT01.pdf)<br>
Bertrand Charpentier<br>
KTH Publicaiton Library (DiVA) 2019

Installation
------------

Install the latest version of cylouvain using ``pip`` ::

    $ pip install python_paris

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
    >>> graph.add_nodes_from(['0', '1', '2', '3', '4', '5'])
    >>> graph.add_edges_from([(0, 1, 1), (0, 2, 1), (1, 2, 1), (2, 3, 1),
                              (3, 4, 1), (3, 5, 1), (4, 5, 1)])

Compute a clustering hierarchy of the nodes using paris::

    >>> from python_paris import paris
    >>> dendrogram = paris(graph)

Compute the best clusters, clusterings and distances::

    >>> best_cluster = best_cluster_cut(dendrogram)
    >>> best_homogneous_clustering = best_homogeneous_cut(dendrogram)
    >>> best_heterogneous_clustering = best_heterogeneous_cut(dendrogram)
    >>> best_distance = best_distance

License
-------

Released under the Apache License 2.0 licence::

   Copyright (C) 2018 Bertrand Charpentier <bercha@kth.se>
