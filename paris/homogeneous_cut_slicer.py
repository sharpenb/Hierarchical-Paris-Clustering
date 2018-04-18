import numpy as np


def clustering_from_homogeneous_cut(D, cut):
    n_nodes = np.shape(D)[0] + 1
    cluster = {i: [i] for i in range(n_nodes)}
    for t in range(cut):
        i = int(D[t][0])
        j = int(D[t][1])
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


def best_homogeneous_cut(D, scoring=lambda w, x, y: w * (np.log(x) - np.log(y))):
    n_nodes = np.shape(D)[0] + 1

    cluster_trees = {t: ClusterTree(t, 1., 1, 0.) for t in range(n_nodes)}
    for t in range(n_nodes - 1):
        i = int(D[t][0])
        j = int(D[t][1])
        left_tree = cluster_trees[i]
        right_tree = cluster_trees[j]

        new_distance = D[t, 2]
        new_size = D[t, 3]

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


def ranking_homogeneous_cuts(D, scoring=lambda w, x, y: w * (np.log(x) - np.log(y))):
    n_nodes = np.shape(D)[0] + 1

    cluster_trees = {t: ClusterTree(t, 1., 1, 0.) for t in range(n_nodes)}
    for t in range(n_nodes - 1):
        i = int(D[t][0])
        j = int(D[t][1])
        left_tree = cluster_trees[i]
        right_tree = cluster_trees[j]

        new_distance = D[t, 2]
        new_size = D[t, 3]

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


def naive_best_homogeneous_cut(D, scoring=lambda x, y: np.log(x) - np.log(y)):
    score = scoring(D[1:, 2], D[:-1, 2])
    best_cut = np.argmax(score) + 1
    best_score = max(score)
    return best_cut, best_score


def naive_ranking_homogeneous_cuts(D, scoring=lambda x, y: np.log(x) - np.log(y)):
    scores = scoring(D[1:, 2], D[:-1, 2])
    ranked_cuts = np.argsort(-scores) + 1
    ranked_scores = sorted(scores, reverse=True)
    return ranked_cuts, ranked_scores


def filter_homogeneous_ranking(ranking, scores, D, threshold=.1, scaling=lambda x: np.log(x)):
    s_index = np.concatenate(([0.], scaling(D[:, 2]) - scaling(D[0, 2])))
    filtered_ranking = []
    filtered_scores = []
    for i, t in enumerate(ranking):
        to_exclude = False
        for s in filtered_ranking:
            if abs(s_index[s] - s_index[t]) < threshold * s_index[s]:
                to_exclude = True
                break
        if not to_exclude:
            filtered_ranking.append(t)
            filtered_scores.append(scores[i])

    return filtered_ranking, filtered_scores
