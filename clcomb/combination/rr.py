from argparse import ArgumentParser
from typing import List, Dict, Tuple
from embeddings import write_trec
from collections import defaultdict

import pandas as pd


def read_trec(file: str) -> pd.DataFrame:
    return pd.read_csv(file, sep='\s+', header=None,
        names=['query_id', 'Q0', 'document_id', 'rank', 'score', 'system'],
        usecols=['query_id', 'document_id', 'rank', 'score'])

def combine_query(query_scores: List[pd.DataFrame]) -> List[Tuple[str, float]]:
    docs = defaultdict(list)
    scores = {}

    for system in query_scores:
        for row in system.itertuples():
            docs[row.document_id].append(row.rr)

    for document, rrs in docs.items():
        scores[document] = sum(rrs)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def combine(systems: List[pd.DataFrame]) -> pd.DataFrame:
    rankings = {}
    queries = defaultdict(list)

    for system in systems:
        system['rr'] = 1. / (system['rank'])
        for query, df in system.groupby('query_id'):
            queries[query].append(df)

    for query, dfs in queries.items():
        rankings[query] = combine_query(dfs)

    return rankings


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--systems', dest='systems', nargs='+', help='trec file for each system you are combining')
    args = parser.parse_args()

    scores = [read_trec(system) for system in args.systems]
    combined = combine(scores)

    print(write_trec(combined))