from typing import Dict, List, Tuple, Callable
from collections import defaultdict
from tqdm import tqdm

import pandas as pd


def write_trec(rankings: Dict[str, List[Tuple[str, float]]]) -> str:
    output = ''
    for query, docs in rankings.items():
        for i, (doc, score) in enumerate(docs):
            output += f'{query} Q0 {doc} {i+1} {score} indri\n'
    return output[:-1]
