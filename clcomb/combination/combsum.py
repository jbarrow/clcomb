from typing import List, Tuple, Dict
from argparse import ArgumentParser
from collections import defaultdict
from tqdm import tqdm
from .util import read_trec, write_trec, combine

import pandas as pd


eps = 1e-6

def combsto_query(query_scores: List[pd.DataFrame]) -> List[Tuple[str, float]]:
    docs = defaultdict(list)
    scores = {}

    for system in query_scores:
        for row in system.itertuples():
            docs[row.document_id].append(row.score)

    for document, mnzs in docs.items():
        scores[document] = sum(mnzs)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--systems', dest='systems', nargs='+', help='trec file for each system you are combining')
    args = parser.parse_args()

    scores = [read_trec(system) for system in tqdm(args.systems)]
    combined = combine(scores, combsto_query)

    print(write_trec(combined))
