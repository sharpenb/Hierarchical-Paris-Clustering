import numpy as np


def clustering_from_distance(dendrogram, distance):
    """
     Given a dendrogram and a distance level, compute the partitions corresponding to the distance level

     Parameters
     ----------
     dendrogram: numpy.array
         Each line of the dendrogram contains the merged nodes, the distance between merged nodes and the number of
         nodes in the new cluster
     cut: int
         The distance level at which the partition is extracted. All the clusters are extracted at this distance

     Returns
     -------
     partition: list of list
         A list of clusters, where each cluster is a list of nodes

     References
     ----------
     -
     """
    n_nodes = np.shape(dendrogram)[0] + 1
    if distance < 0:
        raise ValueError
    cluster = {u: [u] for u in range(n_nodes)}
    for t in range(n_nodes - 1):
        if dendrogram[t, 2] > distance:
            break
        cluster[n_nodes + t] = cluster.pop(int(dendrogram[t][0])) + cluster.pop(int(dendrogram[t][1]))
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


def best_distance(dendrogram, scoring=lambda w, x, y: w * (np.log(x) - np.log(y)), mean=lambda x, y: np.sqrt(x * y)):
    """
     Given a dendrogram and a scoring function, compute the cut level with the best average cluster score with respect
     to the scoring function

     Parameters
     ----------
     dendrogram: numpy.array
         Each line of the dendrogram contains the merged nodes, the distance between merged nodes and the number of
         nodes in the new cluster
     scoring: function
         Function that computes the score of a cluster thanks to its number of nodes (w), its creation distance (x) and
         its merged distance (y)
     mean: function
         Mean used to compute the optimal distance from the distance ranges ([x,y])

     Returns
     -------
     best_distance: int
         Best distance in the dendrogram.

     best_distance_score: double
         Best score obtained by the best distance

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

    best_distance = 0.
    best_distance_score = 0.
    score = 0.
    for t in range(n_nodes - 1):
        if score > best_distance_score:
            best_distance = mean(dendrogram[t - 1, 2], dendrogram[t, 2])
            best_distance_score = score
        score = score - (cluster_trees[n_nodes + t].old_score) + (cluster_trees[n_nodes + t].score)

    return best_distance, best_distance_score


def ranking_distances(dendrogram, scoring=lambda w, x, y: w * (np.log(x) - np.log(y)), mean=lambda x, y: np.sqrt(x * y)):
    """
     Given a dendrogram and a scoring function, compute the ranking of the cut level with the best average cluster score
     with respect to the scoring function

     Parameters
     ----------
     dendrogram: numpy.array
         Each line of the dendrogram contains the merged nodes, the distance between merged nodes and the number of
         nodes in the new cluster
     scoring: function
         Function that computes the score of a cluster thanks to its number of nodes (w), its creation distance (x) and
         its merged distance (y)
     mean: function
         Mean used to compute the optimal distance from the distance ranges ([x,y])

     Returns
     -------
     ranked_distancess: list of int
         Ranking of the distances
     ranked_distance_scores: list of double
         List of the distance scores in the ranking order

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

    distances = np.concatenate(([0.], np.array(mean(dendrogram[1:, 2], dendrogram[:-1, 2]))))
    distance_scores = np.array([ 0. for t in range(n_nodes - 1)])
    score = 0.
    for t in range(n_nodes - 1):
        distance_scores[t] = score
        score = score - (cluster_trees[n_nodes + t].old_score) + (cluster_trees[n_nodes + t].score)

    ranked_indices = np.argsort(-distance_scores)
    ranked_distances = [distances[i] for i in ranked_indices]
    ranked_distance_scores = sorted(list(distance_scores), reverse=True)

    return ranked_distances, ranked_distance_scores
