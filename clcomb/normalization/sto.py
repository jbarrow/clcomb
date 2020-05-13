from typing import List, Tuple, Dict
from argparse import ArgumentParser
from tqdm import tqdm
from .util import write_trec
from pathlib import Path

import numpy as np
import pytrec_eval


eps = 1e-6

def sto_normalize(system: Dict[str, Dict[str, float]], gamma: float) -> Dict[str, List[Tuple[str, float]]]:
    normalized = {}

    for query, scores in system.items():
        per_query = {}

        denominator = sum([(np.exp(score) ** gamma) for score in scores.values()])

        for doc, score in scores.items():
            new_score = (np.exp(score) ** gamma) / denominator
            per_query[doc] = new_score

        normalized[query] = sorted(per_query.items(), key=lambda x: x[1], reverse=True)

    return normalized


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('system', help='trec file for each system you are combining', type=Path)
    args = parser.parse_args()

    with args.system.open() as fp:
        scores = pytrec_eval.parse_run(fp)

    normalized = sto_normalize(scores, gamma=1.0)

    print(write_trec(normalized))
