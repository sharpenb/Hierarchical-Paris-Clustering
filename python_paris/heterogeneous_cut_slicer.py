import numpy as np

def clustering_from_heterogeneous_cut(dendrogram, cut):
    """
     Given a dendrogram and a cut level, compute the heterogeneous partitions corresponding to the cut level

     Parameters
     ----------
     dendrogram: numpy.array
         Each line of the dendrogram contains the merged nodes, the distance between merged nodes and the number of
         nodes in the new cluster.
     cut: list of int
         The cut levels at which the clusters of the partition. Each cluster is extracted at its own cut level.

     Returns
     -------
     partition: list of list
         A list of clusters, where each cluster is a list of nodes.

     References
     ----------
     -
     """
    n_nodes = np.shape(dendrogram)[0] + 1
    for e in cut:
        if e < 0 or e > 2 * n_nodes - 2:
            raise ValueError
    clusters = []
    cluster = {u: [u] for u in range(n_nodes)}
    for t in range(n_nodes):
        if t in cut:
            clusters.append([t])
    for t in range(n_nodes - 1):
        cluster[n_nodes + t] = cluster.pop(int(dendrogram[t][0])) + cluster.pop(int(dendrogram[t][1]))
        if n_nodes + t in cut:
            clusters.append(cluster[n_nodes + t])
    return clusters


class ClusterTree:
    def __init__(self, cluster_label, distance, size, best_score, best_cut):
        self.cluster_label = cluster_label
        self.distance = distance
        self.size = size
        self.best_score = best_score
        self.best_cut = best_cut
        self.left = None
        self.right = None


def best_heterogeneous_cut(dendrogram, scoring=lambda w, x, y: w * (np.log(x) - np.log(y)), to_exclude=set([])):
    """
     Given a dendrogram and a scoring function, compute the heterogeneous cut level with the best average cluster score
     with respect to the scoring function.

     Parameters
     ----------
     dendrogram: numpy.array
         Each line of the dendrogram contains the merged nodes, the distance between merged nodes and the number of
         nodes in the new cluster.
     scoring: function
         Function that computes the score of a cluster thanks to its number of nodes (w), its creation distance (x) and
         its merged distance.
     to_exclude: set of int
         Set of cluster cut to exclude in the evaluaton of the best heterogeneous partition

     Returns
     -------
     best_cut: list of int
         Best heterogeneous cut level in the dendrogram. The best cut level is the cut level with the highest average
         cluster score. The list of int indicates the cluster cuts which composed the heterogeneous cut. They go from 0
         to 2*n-2.

     best_cut_score: double
         Best score obtained by the best heterogeneous cut level

     References
     ----------
     -
     """
    n_nodes = np.shape(dendrogram)[0] + 1
    cluster_trees = {t: ClusterTree(t, 0., 1, 0., [t]) for t in range(n_nodes)}
    for t in range(n_nodes - 1):
        i = int(dendrogram[t][0])
        j = int(dendrogram[t][1])
        left_tree = cluster_trees.pop(i)
        right_tree = cluster_trees.pop(j)

        new_distance = dendrogram[t, 2]
        new_size = dendrogram[t, 3]

        if left_tree.distance > 0.:
            left_tree_score = scoring(left_tree.size, new_distance, left_tree.distance)
        else:
            left_tree_score = 0.
        if left_tree.cluster_label not in to_exclude and left_tree_score > left_tree.best_score:
            left_tree.best_score = left_tree_score
            left_tree.best_cut = [left_tree.cluster_label]

        if right_tree.distance > 0.:
            right_tree_score = scoring(right_tree.size, new_distance, right_tree.distance)
        else:
            right_tree_score = 0.
        if right_tree.cluster_label not in to_exclude and right_tree_score > right_tree.best_score:
            right_tree.best_score = right_tree_score
            right_tree.best_cut = [right_tree.cluster_label]

        new_tree = ClusterTree(n_nodes + t, new_distance, new_size, left_tree.best_score + right_tree.best_score, left_tree.best_cut + right_tree.best_cut)
        new_tree.left = left_tree
        new_tree.right = right_tree
        cluster_trees[n_nodes + t] = new_tree

    best_cut = set(cluster_trees[2 * n_nodes - 2].best_cut)
    best_score = cluster_trees[2 * n_nodes - 2].best_score

    return best_cut, best_score


def ranking_heterogeneous_cuts(dendrogram, k, scoring=lambda w, x, y: w * (np.log(x) - np.log(y))):
    """
     Given a dendrogram and a scoring function, compute the ranking of the heterogeneous cut level with the best average
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
     ranked_cuts: list of list of int
         Ranking of the heterogeneous cut levels. The best cut level is the cut level with the highest average cluster
         score. The list of int indicates the cluster cuts which composed the heterogeneous cut. They go from 0
         to 2*n-2.
     ranked_cut_scores: list of double
         List of the heterogeneous cut level scores in the ranking order.

     References
     ----------
     -
     """
    ranked_cuts = []
    ranked_cut_scores = []
    to_exclude = set()
    for i in range(k):
        best_cut, best_cut_score = best_heterogeneous_cut(dendrogram, scoring=scoring, to_exclude=to_exclude)
        ranked_cuts.append(best_cut)
        ranked_cut_scores.append(best_cut_score)
        to_exclude = to_exclude.union(best_cut)
    return ranked_cuts, ranked_cut_scores
