from typing import Dict, List, Tuple, Callable
from collections import defaultdict
from tqdm import tqdm

import pandas as pd


def read_trec(file: str) -> pd.DataFrame:
    return pd.read_csv(file, sep='\s+', header=None,
        names=['query_id', 'Q0', 'document_id', 'rank', 'score', 'system'],
        usecols=['query_id', 'document_id', 'rank', 'score'])


def write_trec(rankings: Dict[str, List[Tuple[str, float]]]) -> str:
    output = ''
    for query, docs in rankings.items():
        for i, (doc, score) in enumerate(docs):
            output += f'{query} Q0 {doc} {i+1} {score} indri\n'
    return output[:-1]


def combine(systems: List[pd.DataFrame],
            combiner: Callable[[List[pd.DataFrame]], List[Tuple[str, float]]]) -> Dict[str, List[Tuple[str, float]]]:
    rankings = {}
    queries = defaultdict(list)

    for system in systems:
        for query, df in system.groupby('query_id'):
            queries[query].append(df)

    for query, dfs in tqdm(queries.items()):
       rankings[query] = combiner(dfs)

    return rankings
