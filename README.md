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
    
Cite
----

Please cite our paper and my thesis if you use the algorithms or this code in your own work:

```
@inproceedings{paris_clustering,
  TITLE = {{Hierarchical Graph Clustering using Node Pair Sampling}},
  AUTHOR = {Bonald, Thomas and Charpentier, Bertrand and Galland, Alexis and Hollocou, Alexandre},
  URL = {https://hal.archives-ouvertes.fr/hal-01887669},
  BOOKTITLE = {{MLG 2018 - 14th International Workshop on Mining and Learning with Graphs}},
  ADDRESS = {London, United Kingdom},
  SERIES = {MLG 2018 - 14th International Workshop on Mining and Learning with Graphs},
  YEAR = {2018},
  MONTH = Aug,
  PDF = {https://hal.archives-ouvertes.fr/hal-01887669/file/arxiv.pdf},
  HAL_ID = {hal-01887669},
  HAL_VERSION = {v1},
}
```

```
@phdthesis{Charpentier_2019, series={TRITA-EECS-EX}, 
title={Multi-scale clustering in graphs using modularity}, 
url={http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-244847}, 
abstractNote={This thesis provides a new hierarchical clustering algorithm for graphs, named Paris, which can be interpreted through the modularity score and its resolution parameter. The algorithm is agglomerative and based on a simple distance between clusters induced by the probability of sampling node pairs. It tries to approximate the optimal partitions with respect to the modularity score at any resolution in one run.In addition to the Paris hierarchical algorithm, this thesis proposes four algorithms that compute rankings of the sharpest clusters, clusterings and resolutions by processing the hierarchy output by Paris. These algorithms are based on a new measure of stability for clusterings, named sharp-score. Key outcomes of these four algorithms are the possibility to rank clusters, detect sharpest clusterings scale, go beyond the resolution limit and detect relevant resolutions.All these algorithms have been tested on both synthetic and real datasets to illustrate the efficiency of their approaches.}, 
author={Charpentier, Bertrand}, 
year={2019}, 
collection={TRITA-EECS-EX}}
```

License
-------

Released under the Apache License 2.0 licence::

   Copyright (C) 2018 Bertrand Charpentier <bertrand.charpentier@in.tum.de>, <bercha@kth.se>
