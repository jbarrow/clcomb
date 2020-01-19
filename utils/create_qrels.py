from argparse import ArgumentParser
from pathlib import Path


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('files', nargs='+', help='MATERIAL relevance judgements files', type=Path)
    args = parser.parse_args()

    relevant = []

    for file in args.files:
        with file.open() as fp:
            # check if we need to skip header
            header = fp.readline()
            if 'doc_id' not in header:
                relevant.append(header.strip().split())

            for line in fp:
                relevant.append(line.strip().split())

    for query_id, doc_id in relevant:
        print(f'{query_id}\t0\t{doc_id}\t1')
