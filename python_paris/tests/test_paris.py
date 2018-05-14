import unittest
import networkx
from python_paris.paris import *


class TestParis(unittest.TestCase):

    def setUp(self):
        self.weighted_graph = nx.Graph()
        self.weighted_graph.add_nodes_from([0, 1, 2, 3, 4, 5])
        self.weighted_graph.add_weighted_edges_from([(0, 1, 1), (0, 2, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (3, 5, 1),
                                                (4, 5, 1)])
        self.unweighted_graph = nx.Graph()
        self.unweighted_graph.add_nodes_from([0, 1, 2, 3, 4, 5])
        self.unweighted_graph.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5)])

    def test_paris(self):
        dendrogram_weighted = paris(self.weighted_graph)
        dendrogram_unweighted = paris(self.unweighted_graph)

        self.assertEqual(dendrogram_unweighted.any(), dendrogram_weighted.any())
