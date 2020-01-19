from argparse import ArgumentParser
from pathlib import Path
from collections import defaultdict
from typing import Set, Tuple, List, Any, Dict
from tqdm import tqdm
from sklearn.cluster import SpectralClustering

import random
import numpy as np
import pytrec_eval
import statistics


EPSILON = 1e-6


def jaccard_score(s1: Set[Any], s2: Set[Any]) -> float:
    return 1. * len(s1 & s2) / (len(s1 | s2) + EPSILON)


def pairwise_jaccard_scores(matchers: Dict[str, Set[Any]]) -> Tuple[List[str], np.array]:
    matcher_names = list(matchers.keys())
    t = len(matcher_names)
    scores = np.zeros((t, t))

    for i, m1 in tqdm(enumerate(matcher_names)):
        s1 = matchers[m1]
        for j, m2 in enumerate(matcher_names):
            s2 = matchers[m2]
            scores[i, j] = jaccard_score(s1, s2)

    return matcher_names, scores


def cluster(names: List[str], matrix: np.array, n_clusters: int) -> Dict[str, List[str]]:
    clustering = SpectralClustering(n_clusters=n_clusters).fit(matrix)
    clusters = defaultdict(list)
    for name, label in zip(names, clustering.labels_):
        clusters[label].append(name)
    return clusters


def get_average_metric(evaluator: pytrec_eval.RelevanceEvaluator,
                       system: Path,
                       metric: str = 'map') -> float:
    # load the TREC file
    with system.open() as fp:
        run = pytrec_eval.parse_run(fp)
    # run the evaluator over the loaded run
    results = evaluator.evaluate(run)
    # return the average of the desired metric
    return statistics.mean([results[q][metric] for q in results.keys()])


def get_tuples(run: Dict[str, Dict[str, float]]) -> Set[Tuple[str, str]]:
    tuples = set([])
    for query, documents in run.items():
        for document in documents.keys():
            tuples.add((query, document))
    return tuples


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--systems', nargs='+', help='system files to select', type=Path)
    parser.add_argument('--qrels', help='relevance judgements', type=Path)
    parser.add_argument('--sample', help='method to sample from the clusters', choices=['best', 'random'])
    parser.add_argument('--K', help='number of clusters', type=int)
    parser.add_argument('--metric', help='metric to use to select systems', type=str, default='map')
    args = parser.parse_args()

    with args.qrels.open() as fp:
        qrels = pytrec_eval.parse_qrel(fp)

    evaluator = pytrec_eval.RelevanceEvaluator(qrels, { args.metric })

    scores: Dict[str, float] = {
        str(system): get_average_metric(evaluator, system, args.metric)
        for system in args.systems
    }

    relevant_tuples = get_tuples(qrels)

    tuples = {}
    for system in args.systems:
        key = str(system)

        with system.open() as fp:
            run = pytrec_eval.parse_run(fp)

        returned_tuples = get_tuples(run)
        tuples[key] = returned_tuples & relevant_tuples

    names, matrix = pairwise_jaccard_scores(tuples)

    clusters = cluster(names, matrix, args.K)

    for cluster in clusters.values():
        if args.sample == 'best':
            cluster_scores = [(system, scores[str(system)]) for system in cluster]
            print(max(cluster_scores, key=lambda x: x[1])[0])
        else:
            print(random.choice(cluster))
