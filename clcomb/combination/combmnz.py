from typing import List, Tuple, Dict
from argparse import ArgumentParser
from collections import defaultdict
from tqdm import tqdm
from ..util import read_trec, write_trec, combine

import pandas as pd


eps = 1e-6

def combmnz_query(query_scores: List[pd.DataFrame]) -> List[Tuple[str, float]]:
    docs = defaultdict(list)
    scores = {}

    for system in query_scores:
        max_score = max(pd.to_numeric(system.score))
        min_score = min(pd.to_numeric(system.score))

        scorediff = max(max_score - min_score, eps)

        for row in system.itertuples():
            new_score = (row.score - min_score) / scorediff
            docs[row.document_id].append(new_score)

    for document, mnzs in docs.items():
        scores[document] = sum(mnzs) * len(mnzs)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--systems', dest='systems', nargs='+', help='trec file for each system you are combining')
    args = parser.parse_args()

    scores = [read_trec(system) for system in args.systems]
    combined = combine(scores, combmnz_query)

    print(write_trec(combined))
