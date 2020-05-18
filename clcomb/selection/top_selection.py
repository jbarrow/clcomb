from argparse import ArgumentParser
from pathlib import Path
from collections import defaultdict
from typing import Set, Tuple, List, Any, Dict
from tqdm import tqdm
from sklearn.cluster import SpectralClustering
from .similarity import load_comparison

import random
import numpy as np
import pytrec_eval
import statistics


def get_average_metric(evaluator: pytrec_eval.RelevanceEvaluator,
                       system: Path,
                       metric: str = 'map') -> float:
    # load the TREC file
    with system.open() as fp:
        run = pytrec_eval.parse_run(fp)
    # run the evaluator over the loaded run
    results = evaluator.evaluate(run)
    # return the average of the desired metric
    return statistics.mean([results[q][metric] for q in results.keys()])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--systems', nargs='+', help='system files to select', type=Path)
    parser.add_argument('--qrels', help='relevance judgements', type=Path)
    parser.add_argument('--K', help='number of clusters', nargs='+', type=int)
    parser.add_argument('--metric', help='metric to use to select systems', type=str, default='map')
    parser.add_argument('--output-dir', help='directory to output the selected systems to', type=Path)
    args = parser.parse_args()

    with args.qrels.open() as fp:
        qrels = pytrec_eval.parse_qrel(fp)

    evaluator = pytrec_eval.RelevanceEvaluator(qrels, { args.metric })

    scores: List[Tuple[str, float]] = [
        (str(system), get_average_metric(evaluator, system, args.metric))
        for system in tqdm(args.systems)
    ]

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    for k in args.K:
        output_file = 'top_{}.txt'.format(k)
        output_file = args.output_dir / output_file

        with output_file.open('w') as fp:
            for name, _ in scores[:k]:
                fp.write(name)
                fp.write('\n')
