import unittest
from python_paris.heterogeneous_cut_slicer import *


class TestHeterogeneoousCutSlicer(unittest.TestCase):

    def setUp(self):
            self.dendrogram = np.array([[0, 1, 1., 2],
                                        [2, 3, 2., 2],
                                        [4, 5, 4., 4]])

    def test_clustering_from_cluster_cut(self):
        c = clustering_from_heterogeneous_cut(self.dendrogram, set([0, 1, 2, 3]))
        self.assertEqual(c, [[0], [1], [2], [3]])
        c = clustering_from_heterogeneous_cut(self.dendrogram, set([2, 3, 4]))
        self.assertEqual(c, [[2], [3], [0, 1]])
        c = clustering_from_heterogeneous_cut(self.dendrogram, set([0, 1, 5]))
        self.assertEqual(c, [[0], [1], [2, 3]])
        c = clustering_from_heterogeneous_cut(self.dendrogram, set([4, 5]))
        self.assertEqual(c, [[0, 1], [2, 3]])
        c = clustering_from_heterogeneous_cut(self.dendrogram, set([6]))
        self.assertEqual(c, [[0, 1, 2, 3]])

        with self.assertRaises(ValueError):
            clustering_from_heterogeneous_cut(self.dendrogram, set([-1]))

        with self.assertRaises(ValueError):
            clustering_from_heterogeneous_cut(self.dendrogram, set([7]))

    def test_best_cluster_cut(self):
        cut, cut_score = best_heterogeneous_cut(self.dendrogram)
        c = clustering_from_heterogeneous_cut(self.dendrogram, cut)
        self.assertEqual(c, [[0, 1], [2, 3]])


    def test_ranking_cluster_cuts(self):
        ranked_cuts, ranked_cut_scores = ranking_heterogeneous_cuts(self.dendrogram, k=2)
        c = clustering_from_heterogeneous_cut(self.dendrogram, ranked_cuts[0])
        self.assertEqual(c, [[0, 1], [2, 3]])
        c = clustering_from_heterogeneous_cut(self.dendrogram, ranked_cuts[1])
        self.assertEqual(c, [[0], [1], [2], [3]])
