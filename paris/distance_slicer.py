import numpy as np


def clustering_from_distance(D, distance):
    n_nodes = np.shape(D)[0] + 1
    cluster = {u: [u] for u in range(n_nodes)}
    for t in range(n_nodes - 1):
        if D[t, 2] > distance:
            break
        cluster[n_nodes + t] = cluster.pop(int(D[t][0])) + cluster.pop(int(D[t][1]))
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


def best_distance(D, scoring=lambda w, x, y: w * (np.log(x) - np.log(y)), mean=lambda x, y: np.sqrt(x*y)):
    n_nodes = np.shape(D)[0] + 1

    cluster_trees = {t: ClusterTree(t, 0, 1, 0.) for t in range(n_nodes)}
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

    best_distance = 0.
    best_distance_score = 0.
    score = 0.
    for t in range(n_nodes - 1):
        if score > best_distance_score:
            best_distance = mean(D[t - 1, 2], D[t, 2])
            best_distance_score = score
        score = score - (cluster_trees[n_nodes + t].old_score) + (cluster_trees[n_nodes + t].score)

    return best_distance, best_distance_score


def ranking_distances(D, scoring=lambda w, x, y: w * (np.log(x) - np.log(y)), mean=lambda x, y: np.sqrt(x*y)):
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

    distances = np.concatenate(([0.], np.array(mean(D[1:, 2], D[:-1, 2]))))
    distance_scores = np.array([ 0. for t in range(n_nodes - 1)])
    score = 0.
    for t in range(n_nodes - 1):
        distance_scores[t] = score
        score = score - (cluster_trees[n_nodes + t].old_score) + (cluster_trees[n_nodes + t].score)

    ranked_indices = np.argsort(-distance_scores)
    ranked_distances = [distances[i] for i in ranked_indices]
    ranked_distance_scores = sorted(list(distance_scores), reverse=True)

    return ranked_distances, ranked_distance_scores


def naive_best_distance(D, scoring=lambda x, y: np.log(x) - np.log(y), mean=lambda x, y: np.sqrt(x*y)):
    distances = np.array(mean(D[1:, 2], D[:-1, 2]))
    score = scoring(D[1:, 2], D[:-1, 2])
    best_distance = distances[np.argmax(score)]
    best_distance_score = max(score)
    return best_distance, best_distance_score


def naive_ranking_distances(D, scoring=lambda x, y: np.log(x) - np.log(y), mean=lambda x, y: np.sqrt(x*y)):
    mean_distances = np.array(mean(D[1:, 2], D[:-1, 2]))
    distance_scores = scoring(D[1:, 2], D[:-1, 2])
    ranked_indices = np.argsort(-distance_scores)
    ranked_distances = [mean_distances[i] for i in ranked_indices]
    ranked_distance_scores = sorted(list(distance_scores), reverse=True)
    return ranked_distances, ranked_distance_scores


def filter_distance_ranking(ranking, scores, D, threshold=.1, scaling=lambda x: np.log(x)):
    scaling_e_0 = scaling(D[0, 2])
    filtered_ranking = []
    filtered_scores = []
    for i, d in enumerate(ranking):
        to_exclude = False
        for e in filtered_ranking:
            if abs(scaling(e) - scaling(d)) < threshold * (scaling(e) - scaling_e_0):
                to_exclude = True
                break
        if not to_exclude:
            filtered_ranking.append(d)
            filtered_scores.append(scores[i])

    return filtered_ranking, filtered_scores
