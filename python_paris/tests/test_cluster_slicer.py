import unittest
from python_paris.cluster_cut_slicer import *


class TestClusterSlicer(unittest.TestCase):

    def setUp(self):
            self.dendrogram = np.array([[0, 1, 1., 2],
                                        [2, 3, 2., 2],
                                        [4, 5, 4., 4]])

    def test_clustering_from_cluster_cut(self):
        c = clustering_from_cluster_cut(self.dendrogram, 0)
        self.assertEqual(c, [0])
        c = clustering_from_cluster_cut(self.dendrogram, 1)
        self.assertEqual(c, [1])
        c = clustering_from_cluster_cut(self.dendrogram, 2)
        self.assertEqual(c, [2])
        c = clustering_from_cluster_cut(self.dendrogram, 3)
        self.assertEqual(c, [3])
        c = clustering_from_cluster_cut(self.dendrogram, 4)
        self.assertEqual(c, [0, 1])
        c = clustering_from_cluster_cut(self.dendrogram, 5)
        self.assertEqual(c, [2, 3])
        c = clustering_from_cluster_cut(self.dendrogram, 6)
        self.assertEqual(c, [0, 1, 2, 3])

        with self.assertRaises(ValueError):
            clustering_from_cluster_cut(self.dendrogram, -1)
        with self.assertRaises(ValueError):
            clustering_from_cluster_cut(self.dendrogram, 7)

    def test_best_cluster_cut(self):
        cut, cut_score = best_cluster_cut(self.dendrogram)
        self.assertEqual(cut, 4)

    def test_ranking_cluster_cuts(self):
        ranked_cuts, ranked_scores = ranking_cluster_cuts(self.dendrogram)
        self.assertEqual(ranked_cuts, [4, 5, 0, 1, 2, 3])
