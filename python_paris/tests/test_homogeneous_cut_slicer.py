import unittest
from python_paris.homogeneous_cut_slicer import *


class TestHomogeneoousCutSlicer(unittest.TestCase):

    def setUp(self):
            self.dendrogram = np.array([[0, 1, 1., 2],
                                        [2, 3, 2., 2],
                                        [4, 5, 4., 4]])

    def test_clustering_from_cluster_cut(self):
        c = clustering_from_homogeneous_cut(self.dendrogram, 0)
        self.assertEqual(c, [[0], [1], [2], [3]])
        c = clustering_from_homogeneous_cut(self.dendrogram, 1)
        self.assertEqual(c, [[2], [3], [0, 1]])
        c = clustering_from_homogeneous_cut(self.dendrogram, 2)
        self.assertEqual(c, [[0, 1], [2, 3]])
        c = clustering_from_homogeneous_cut(self.dendrogram, 3)
        self.assertEqual(c, [[0, 1, 2, 3]])

        with self.assertRaises(ValueError):
            clustering_from_homogeneous_cut(self.dendrogram, -1)

        with self.assertRaises(ValueError):
            clustering_from_homogeneous_cut(self.dendrogram, 4)

    def test_best_cluster_cut(self):
        cut, cut_score = best_homogeneous_cut(self.dendrogram)
        c = clustering_from_homogeneous_cut(self.dendrogram, cut)
        self.assertEqual(c, [[0, 1], [2, 3]])


    def test_ranking_cluster_cuts(self):
        ranked_cuts, ranked_cut_scores = ranking_homogeneous_cuts(self.dendrogram)
        c = clustering_from_homogeneous_cut(self.dendrogram, ranked_cuts[0])
        self.assertEqual(c, [[0, 1], [2, 3]])
        c = clustering_from_homogeneous_cut(self.dendrogram, ranked_cuts[1])
        self.assertEqual(c, [[2], [3], [0, 1]])
        c = clustering_from_homogeneous_cut(self.dendrogram, ranked_cuts[2])
        self.assertEqual(c, [[0], [1], [2], [3]])
