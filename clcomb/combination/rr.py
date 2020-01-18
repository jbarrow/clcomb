from argparse import ArgumentParser
from typing import List, Dict, Tuple
from collections import defaultdict
from .util import read_trec, write_trec, combine

import pandas as pd


def rr_query(query_scores: List[pd.DataFrame]) -> List[Tuple[str, float]]:
    docs = defaultdict(list)
    scores = {}

    for system in query_scores:
        system['rr'] = 1. / (system['rank'])
        for row in system.itertuples():
            docs[row.document_id].append(row.rr)

    for document, rrs in docs.items():
        scores[document] = sum(rrs)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
    

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--systems', dest='systems', nargs='+', help='trec file for each system you are combining')
    args = parser.parse_args()

    scores = [read_trec(system) for system in args.systems]
    combined = combine(scores, rr_query)

    print(write_trec(combined))
