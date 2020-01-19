from argparse import ArgumentParser
from pathlib import Path

import numpy as np


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--systems', nargs='+', help='system files to select', type=Path)
    parser.add_argument('--N', help='number of files to combine', type=int)
    args = parser.parse_args()

    systems = list(args.systems)

    for system in np.random.choice(systems, args.N, replace=False):
        print(system)
