import numpy as np

def clustering_from_heterogeneous_cut(D, cut):
    clusters = []
    n_nodes = np.shape(D)[0] + 1
    cluster = {u: [u] for u in range(n_nodes)}
    for t in range(n_nodes):
        if t in cut:
            clusters.append([t])
    for t in range(n_nodes - 1):
        cluster[n_nodes + t] = cluster.pop(int(D[t][0])) + cluster.pop(int(D[t][1]))
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


def best_heterogeneous_cut(D, scoring=lambda w, x, y: w * (np.log(x) - np.log(y)), to_exclude=set([])):
    n_nodes = np.shape(D)[0] + 1
    cluster_trees = {t: ClusterTree(t, 1., 1, 0., [t]) for t in range(n_nodes)}
    for t in range(n_nodes - 1):
        i = int(D[t][0])
        j = int(D[t][1])
        left_tree = cluster_trees.pop(i)
        right_tree = cluster_trees.pop(j)

        new_distance = D[t, 2]
        new_size = D[t, 3]

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


def ranking_heterogeneous_cuts(D, k, scoring=lambda w, x, y: w * (np.log(x) - np.log(y))):
    ranked_cuts = []
    ranked_cut_scores = []
    to_exclude = set()
    for i in range(k):
        best_cut, best_cut_score = best_heterogeneous_cut(D, scoring=scoring, to_exclude=to_exclude)
        ranked_cuts.append(best_cut)
        ranked_cut_scores.append(best_cut_score)
        to_exclude = to_exclude.union(best_cut)
    return ranked_cuts, ranked_cut_scores
