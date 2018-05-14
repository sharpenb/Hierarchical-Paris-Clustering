import unittest
from python_paris.distance_slicer import *


class TestDistanceSlicer(unittest.TestCase):

    def setUp(self):
            self.dendrogram = np.array([[0, 1, 1., 2],
                                        [2, 3, 2., 2],
                                        [4, 5, 4., 4]])

    def test_clustering_from_cluster_cut(self):
        c = clustering_from_distance(self.dendrogram, 0.)
        self.assertEqual(c, [[0], [1], [2], [3]])
        c = clustering_from_distance(self.dendrogram, 1.5)
        self.assertEqual(c, [[2], [3], [0, 1]])
        c = clustering_from_distance(self.dendrogram, 3)
        self.assertEqual(c, [[0, 1], [2, 3]])
        c = clustering_from_distance(self.dendrogram, 5.)
        self.assertEqual(c, [[0, 1, 2, 3]])

        with self.assertRaises(ValueError):
            clustering_from_distance(self.dendrogram, -1)

    def test_best_cluster_cut(self):
        distance, distance_score = best_distance(self.dendrogram)
        c = clustering_from_distance(self.dendrogram, distance)
        self.assertEqual(c, [[0, 1], [2, 3]])


    def test_ranking_cluster_cuts(self):
        ranked_distances, ranked_distance_scores = ranking_distances(self.dendrogram)
        c = clustering_from_distance(self.dendrogram, ranked_distances[0])
        self.assertEqual(c, [[0, 1], [2, 3]])
        c = clustering_from_distance(self.dendrogram, ranked_distances[1])
        self.assertEqual(c, [[2], [3], [0, 1]])
        c = clustering_from_distance(self.dendrogram, ranked_distances[2])
        self.assertEqual(c, [[0], [1], [2], [3]])
