import numpy as np


def clustering_from_homogeneous_cut(dendrogram, cut):
    """
     Given a dendrogram and a cut level, compute the homogeneous partition corresponding to the cut level.

     Parameters
     ----------
     dendrogram: numpy.array
         Each line of the dendrogram contains the merged nodes, the distance between merged nodes and the number of
         nodes in the new cluster.
     cut: int
         The cut level at which the partition is extracted. All the clusters are extracted at this cut level.

     Returns
     -------
     partition: list of list
         A list of clusters, where each cluster is a list of nodes.

     References
     ----------
     -
     """
    n_nodes = np.shape(dendrogram)[0] + 1
    if cut < 0 or cut > n_nodes - 1:
        raise ValueError
    cluster = {i: [i] for i in range(n_nodes)}
    for t in range(cut):
        i = int(dendrogram[t][0])
        j = int(dendrogram[t][1])
        cluster[n_nodes + t] = cluster.pop(i) + cluster.pop(j)
    clusters = [cluster[c] for c in cluster]
    return clusters


class ClusterTree:
    def __init__(self, cluster_label, distance, size, old_score):
        self.cluster_label = cluster_label
        self.distance = distance
        self.size = size
        self.score = 0.
        self.old_score = old_score
        self.left = None
        self.right = None


def best_homogeneous_cut(dendrogram, scoring=lambda w, x, y: w * (np.log(x) - np.log(y))):
    """
     Given a dendrogram and a scoring function, compute the homogeneous cut level with the best average cluster score
     with respect to the scoring function.

     Parameters
     ----------
     dendrogram: numpy.array
         Each line of the dendrogram contains the merged nodes, the distance between merged nodes and the number of
         nodes in the new cluster.
     scoring: function
         Function that computes the score of a cluster thanks to its number of nodes (w), its creation distance (x) and
         its merged distance (y).

     Returns
     -------
     best_cut: int
         Best homogeneous cut in the dendrogram. The best homogeneous cut is the cut level with the highest average
         cluster score. The cut level can go from 0 to n - 1 with n the number of nodes. The cut t is the partition
         created after t merges.

     best_cut_score: double
         Best score obtained by the best homogeneous cut level

     References
     ----------
     -
     """
    n_nodes = np.shape(dendrogram)[0] + 1
    cluster_trees = {t: ClusterTree(t, 0., 1, 0.) for t in range(n_nodes)}
    for t in range(n_nodes - 1):
        i = int(dendrogram[t][0])
        j = int(dendrogram[t][1])
        left_tree = cluster_trees[i]
        right_tree = cluster_trees[j]

        new_distance = dendrogram[t, 2]
        new_size = dendrogram[t, 3]

        if left_tree.distance > 0.:
            left_tree.score = scoring(left_tree.size, new_distance, left_tree.distance)
        else:
            left_tree.score = 0.

        if right_tree.distance > 0.:
            right_tree.score = scoring(right_tree.size, new_distance, right_tree.distance)
        else:
            right_tree.score = 0.

        new_tree = ClusterTree(n_nodes + t, new_distance, new_size, left_tree.score + right_tree.score)
        new_tree.left = left_tree
        new_tree.right = right_tree
        cluster_trees[n_nodes + t] = new_tree

    best_cut = 0
    best_score = 0.
    score = 0.
    for t in range(n_nodes - 1):
        if score > best_score:
            best_cut = t
            best_score = score
        score = score - (cluster_trees[n_nodes + t].old_score) + (cluster_trees[n_nodes + t].score)

    return best_cut, best_score


def ranking_homogeneous_cuts(dendrogram, scoring=lambda w, x, y: w * (np.log(x) - np.log(y))):
    """
     Given a dendrogram and a scoring function, compute the ranking of the homogeneous cut level with the best average
     cluster score with respect to the scoring function.

     Parameters
     ----------
     dendrogram: numpy.array
         Each line of the dendrogram contains the merged nodes, the distance between merged nodes and the number of
         nodes in the new cluster.
     scoring: function
         Function that computes the score of a cluster thanks to its number of nodes (w), its creation distance (x) and
         its merged distance.

     Returns
     -------
     ranked_cuts: list of int
         Ranking of the homogeneous cut levels. The best cut level is the cut level with the highest average cluster
         score. The cut level can go from 0 to n - 1 with n the number of nodes. The cut t is the partition created
         after t merges.
     ranked_cut_scores: list of double
         List of the cut level scores in the ranking order.

     References
     ----------
     -
     """
    n_nodes = np.shape(dendrogram)[0] + 1
    cluster_trees = {t: ClusterTree(t, 0., 1, 0.) for t in range(n_nodes)}
    for t in range(n_nodes - 1):
        i = int(dendrogram[t][0])
        j = int(dendrogram[t][1])
        left_tree = cluster_trees[i]
        right_tree = cluster_trees[j]

        new_distance = dendrogram[t, 2]
        new_size = dendrogram[t, 3]

        if left_tree.distance > 0.:
            left_tree.score = scoring(left_tree.size, new_distance, left_tree.distance)
        else:
            left_tree.score = 0.

        if right_tree.distance > 0.:
            right_tree.score = scoring(right_tree.size, new_distance, right_tree.distance)
        else:
            right_tree.score = 0.

        new_tree = ClusterTree(n_nodes + t, new_distance, new_size, left_tree.score + right_tree.score)
        new_tree.left = left_tree
        new_tree.right = right_tree
        cluster_trees[n_nodes + t] = new_tree

    cuts = [t for t in range(n_nodes - 1)]
    cut_scores = {t: 0. for t in range(n_nodes - 1)}
    score = 0.
    for t in range(n_nodes - 1):
        cut_scores[t] = score
        score = score - (cluster_trees[n_nodes + t].old_score) + (cluster_trees[n_nodes + t].score)

    ranked_cuts = sorted(cuts, key=lambda x: cut_scores[x], reverse=True)
    ranked_cut_scores = sorted(list(cut_scores.values()), reverse=True)

    return ranked_cuts, ranked_cut_scores
