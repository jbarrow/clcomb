"""
Script to gather experiment results.
"""
from argparse import ArgumentParser

import itertools
import glob
import json
import csv
import os

SCORES_FILE='scores_by_type.csv'

def parse_file(contents):
    results = {}
    chunks = itertools.groupby(contents.split('\n'), lambda x: bool(x.strip()))
    for has_content, chunk in chunks:
        if not has_content: continue
        results_type, values = parse_results_chunk(list(chunk))
        results[results_type] = values
    return results

def parse_config(contents):
    config = json.loads(contents)
    return config['matcher']['configurations'][0]['index_type']

def parse_results_chunk(results_chunk):
    header = results_chunk[0].strip()
    keys = header.split(',')
    keys[0], results_type = keys[0].split(' / ')

    lines = []
    for line in results_chunk[1:]:
        results = {k: v for k, v in zip(keys, line.strip().split(','))}
        lines.append(results)

    return results_type, lines

def walk_experiments_directory(dir, type, writer):
    experimental_results = {}
    for root, dirs, files in os.walk(dir):
        if SCORES_FILE in files:
            file_path = os.path.join(root, SCORES_FILE)
            json_path = list(glob.glob(os.path.join(root, '../*.json')))[0]
            with open(json_path) as fp:
                name = os.path.basename(json_path)
                index = parse_config(fp.read())
            with open(file_path) as fp:
                output_results(name, index, file_path, parse_file(fp.read()), type, writer)

def output_results(experiment_name, index_type, directory, results, type, writer):
    for result_type, values in results.items():
        if result_type == type:
            appended = []
            for row in values:
                row['Name'] = experiment_name
                row['Experiment_Directory'] = directory
                row['Type'] = result_type
                row['Index_Type'] = index_type
                appended.append(row)

            writer.writerows(appended)
            #print(result_type, values[0].keys())

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('experiment_directory')
    parser.add_argument('--types', nargs='+', default=['text', 'audio', 'text+audio'])
    parser.add_argument('--prefix')
    args = parser.parse_args()

    for type in args.types:
        filename = type + '.csv'
        if args.prefix:
            filename = args.prefix + '_' + filename

        with open(filename, 'w') as fp:
            writer = csv.DictWriter(fp, fieldnames=['Name', 'Type', 'Index_Type', 'Query_Type', 'Queries', 'P_miss', 'P_fa', 'AQWV', 'MQWV_tied', 'MQWV_cutoff', 'Experiment_Directory'])
            writer.writeheader()

            output = walk_experiments_directory(
                dir=args.experiment_directory,
                type=type,
                writer=writer
            )
