from typing import Dict, List, Tuple

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
    return output
