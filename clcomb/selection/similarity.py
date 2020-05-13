import numpy as np
import pandas as pd
import pytrec_eval

from tqdm import tqdm
from typing import Dict, List, Tuple, Set, Any
from argparse import ArgumentParser
from pathlib import Path
from scipy.stats import pearsonr, kendalltau, spearmanr

TRECOutput = Dict[str, Dict[str, float]]
EPSILON = 1e-6

def pearson_correlation(a: TRECOutput, b: TRECOutput, join: str) -> np.array:
    # start by computing the union of all queries for which a and b have
    # returned something
    all_queries = set(a.keys()) | set(b.keys())
    # initialize the output
    scores = np.zeros(len(all_queries))

    for i, query in enumerate(all_queries):
        if query not in a or query not in b:
            # if one of the system doesn't have output, score is automatically 0
            scores[i] = 0.
            continue

        # the "unreturned" value if we join with union
        min_a = min(a[query].values())
        min_b = min(b[query].values())

        documents_a = a[query]
        documents_b = b[query]

        if join == 'intersection':
            documents = list(set(documents_a.keys()) & set(documents_b.keys()))
        else:
            documents = list(set(documents_a.keys()) | set(documents_b.keys()))

        scores_a = np.array([a[query].get(document, min_a) for document in documents])
        scores_b = np.array([b[query].get(document, min_b) for document in documents])

        scores[i] = pearsonr(scores_a, scores_b)[0]

        if np.isnan(scores[i]):
            if (len(documents_a) == 0 and len(documents_b) == 0) or sorted(scores_a) == sorted(scores_b):
                scores[i] = 1
            else:
                scores[i] = 0

    return scores


def spearman_correlation(a: TRECOutput, b: TRECOutput, join: str) -> np.array:
    # start by computing the union of all queries for which a and b have
    # returned something
    all_queries = set(a.keys()) | set(b.keys())
    # initialize the output
    scores = np.zeros(len(all_queries))

    for i, query in enumerate(all_queries):
        if query not in a or query not in b:
            # if one of the system doesn't have output, score is automatically 0
            scores[i] = 0.
            continue

        # the "unreturned" value if we join with union
        min_a = len(a[query])+1
        min_b = len(b[query])+1

        documents_a = a[query]
        documents_b = b[query]

        ranked_a = {doc: i+1 for i, (doc, _) in enumerate(sorted(a[query].items(), key=lambda x: x[1]))}
        ranked_b = {doc: i+1 for i, (doc, _) in enumerate(sorted(b[query].items(), key=lambda x: x[1]))}


        if join == 'intersection':
            documents = list(set(documents_a.keys()) & set(documents_b.keys()))
        else:
            documents = list(set(documents_a.keys()) | set(documents_b.keys()))

        # rank the documents
        ranks_a = np.array([ranked_a.get(document, min_a) for document in documents])
        ranks_b = np.array([ranked_b.get(document, min_b) for document in documents])

        scores[i] = spearmanr(ranks_a, ranks_b)[0]

        if np.isnan(scores[i]):
            if (len(documents_a) == 0 and len(documents_b) == 0) or len(set(ranked_a.items()) ^ set(ranked_b.items())) == 0:
                scores[i] = 1
            else:
                scores[i] = 0

    return scores


def kendalls_tau(a: TRECOutput, b: TRECOutput, join: str) -> np.array:
    # start by computing the union of all queries for which a and b have
    # returned something
    all_queries = set(a.keys()) | set(b.keys())
    # initialize the output
    scores = np.zeros(len(all_queries))

    for i, query in enumerate(all_queries):
        if query not in a or query not in b:
            # if one of the system doesn't have output, score is automatically 0
            scores[i] = 0.
            continue

        # the "unreturned" value if we join with union
        min_a = len(a[query])+1
        min_b = len(b[query])+1

        documents_a = a[query]
        documents_b = b[query]

        ranked_a = {doc: i+1 for i, (doc, _) in enumerate(sorted(a[query].items(), key=lambda x: x[1]))}
        ranked_b = {doc: i+1 for i, (doc, _) in enumerate(sorted(b[query].items(), key=lambda x: x[1]))}


        if join == 'intersection':
            documents = list(set(documents_a.keys()) & set(documents_b.keys()))
        else:
            documents = list(set(documents_a.keys()) | set(documents_b.keys()))

        # rank the documents
        ranks_a = np.array([ranked_a.get(document, min_a) for document in documents])
        ranks_b = np.array([ranked_b.get(document, min_b) for document in documents])

        scores[i] = kendalltau(ranks_a, ranks_b)[0]

        if np.isnan(scores[i]):
            if (len(documents_a) == 0 and len(documents_b) == 0) or len(set(ranked_a.items()) ^ set(ranked_b.items())) == 0:
                scores[i] = 1
            else:
                scores[i] = 0

    return scores

def cognitive_diversity(a: TRECOutput, b: TRECOutput, join: str) -> np.array:
    return np.zeros(10)


def jaccard_score(a: TRECOutput, b: TRECOutput, join: str) -> np.array:
    # start by computing the union of all queries for which a and b have
    # returned something
    all_queries = set(a.keys()) | set(b.keys())
    # initialize the output
    scores = np.zeros(len(all_queries))

    for i, query in enumerate(all_queries):
        if query not in a or query not in b:
            # if one of the system doesn't have output, score is automatically 0
            scores[i] = 0.
            continue

        documents_a = set(a[query].keys())
        documents_b = set(b[query].keys())

        scores[i] = jaccard(documents_a, documents_b)

    return scores


def jaccard(s1: Set[Any], s2: Set[Any]) -> float:
    return 1. * len(s1 & s2) / (len(s1 | s2) + EPSILON)


def pairwise_comparison(systems: Dict[str, TRECOutput],
                        metric: str,
                        join: str = 'union',
                        aggregate: str = 'average') -> Tuple[List[str], np.array]:
    """
    Function to compute the pairwise similarities between a collection of
    systems. It takes:

    - systems: Dict[str, pd.DataFrame] - the TREC output of the systems to be
        compared
    - metric: str (jaccard|kendall|spearman|cognitive_diversity) - the metric
        to be computed
    - join: str (intersection|union) - for the metrics that require, how to
        resolve returned lists of different lengths or documents
    - aggregate: str (average) - how to aggregate the query-wise similarity
        comparisons. I intend to eventually support a "none" option.

    It then returns a tuple, where the first returned item is the ordered list
    of system names, and the second is the array of similarities (or similarity
    vectors, if no aggregation method is used).
    """

    _dispatch = {
        'jaccard': jaccard_score,
        'kendall': kendalls_tau,
        'pearson': pearson_correlation,
        'spearman': spearman_correlation,
        'cognitive_diversity': cognitive_diversity
    }

    assert metric in _dispatch.keys()
    assert aggregate == 'average'
    assert join in ['intersection', 'union']

    # get the list of matcher names
    matcher_names = list(matchers.keys())
    # total number of matchers
    t = len(matcher_names)
    # initialize the return matrix
    scores = np.zeros((t, t))

    for i, matcher_a in tqdm(enumerate(matcher_names)):
        for j in range(i, len(matcher_names)):
            matcher_b = matcher_names[j]
            # compute the pairwise score for matchers a and b
            pairwise_score = _dispatch[metric](matchers[matcher_a], matchers[matcher_b], join)
            # add the aggregated score to the matrix
            aggregate_score = np.mean(pairwise_score)
            # assign it to the two cells in the matrix
            scores[i, j] = aggregate_score
            scores[j, i] = aggregate_score

    return matcher_names, scores


def save_comparison():
    pass

def load_comparison():
    pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--systems', nargs='+', help='system files to select', type=Path)
    parser.add_argument('--metric', help='which metric to compute', default='pearson', type=str)
    parser.add_argument('--join', help='how to join pairwise systems', default='intersection', type=str)
    args = parser.parse_args()

    matchers = {}

    for system in tqdm(args.systems):
        key = str(system)

        with system.open() as fp:
            run = pytrec_eval.parse_run(fp)

        matchers[key] = run

    print(pairwise_comparison(matchers, metric=args.metric, join=args.join))
