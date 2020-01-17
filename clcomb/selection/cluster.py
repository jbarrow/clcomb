"""
Script to gather experiment results.
"""
from argparse import ArgumentParser
from pathlib import Path
from collections import defaultdict
from typing import Set, Tuple, List, Any, Dict
from tqdm import tqdm
from sklearn.cluster import SpectralClustering

import numpy as np
import csv


def get_experiment_from_config(config: Path) -> Path:
    """ function to strip .json extension """
    return Path(str(config)[:-len(config.suffix)])

def read_trec_docs(trec_file: Path) -> List[str]:
    docs: List[str] = []
    with trec_file.open() as fp:
        for line in fp:
            docs.append(line.strip().split()[2])
    return docs

def jaccard_score(s1: Set[Any], s2: Set[Any]) -> float:
    return 1. * len(s1 & s2) / len(s1 | s2)

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


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('experiment_directories', nargs='+', type=Path)
    parser.add_argument('--qrels', nargs='+', type=Path)
    args = parser.parse_args()

    queries: Set[Tuple[str, str]] = set([])
    for qrels_file in args.qrels:
        with qrels_file.open() as fp:
            q0, d0 = fp.readline().strip().split()
            if q0 != 'query_id':
                queries.add((q0, d0))
            for line in fp:
                if not line.strip(): continue
                q, d = line.strip().split()
                queries.add((q, d))

    matchers = defaultdict(set)

    for experiment_directory in args.experiment_directories:
        configs = list(experiment_directory.glob('*.json'))
        for config in tqdm(configs):
            experiment_directory = get_experiment_from_config(config)
            results = experiment_directory.glob('**/*.trec')
            matcher = config.stem

            for query_file in results:
                query = query_file.stem.split('-')[-1]
                docs = set([(query, doc) for doc in read_trec_docs(query_file)])
                correct_docs = docs & queries
                matchers[matcher].update(correct_docs)

    names, matrix = pairwise_jaccard_scores(matchers)
    np.savetxt('output.txt', matrix, delimiter='\t')

    with open('names.txt', 'w') as fp:
        for name in names:
            fp.write(name + '\n')

    clustering = SpectralClustering().fit(matrix)
    clusters = defaultdict(list)
    for name, label in zip(names, clustering.labels_):
        clusters[label].append(name)

    with open('clusters.txt', 'w') as fp:
        for label, cluster in clusters.items():
            fp.write('\t'.join(cluster))
            fp.write('\n')

"""
So, what's the process here?

    1. read in all the TREC files in UMD-CLIR-workQMDir.
        => thankfully, this can be quickly done just by looking for *.trec
        => check
    2. read in the positive document names from the appropriate NIST-data folder
        => check
    3. for each matcher, compute an intersection of tuples (query_id, document_id)
        => check
    4. for each set of correct tuples, compute a pairwise Jaccard index
        => check
    5. output the pairwise Jaccard index as a matrix, which can be viewed using PCA on projector.tensorflow.org
        => check
    6. additionally, cluster the matchers using scikit-learn
        => check
"""
