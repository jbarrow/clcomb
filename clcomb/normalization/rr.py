from typing import List, Tuple, Dict
from argparse import ArgumentParser
from tqdm import tqdm
from .util import write_trec
from pathlib import Path

import pytrec_eval


eps = 1e-6

def borda_normalize(system: Dict[str, Dict[str, float]]) -> Dict[str, List[Tuple[str, float]]]:
    normalized = {}

    for query, scores in system.items():
        per_query = {}

        # system['rr'] = 1. / (system['rank'])

        for doc, score in scores.items():
            # TODO: COMPUTE RR SCORE
            new_score = 0.
            per_query[doc] = new_score

        normalized[query] = sorted(per_query.items(), key=lambda x: x[1], reverse=True)

    return normalized


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('system', help='trec file for each system you are combining', type=Path)
    args = parser.parse_args()

    with args.system.open() as fp:
        scores = pytrec_eval.parse_run(fp)

    normalized = borda_normalize(scores)

    print(write_trec(normalized))
