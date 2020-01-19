# clcomb

This repository contains the code to replicate the combination experiments in "Evidence Combination for Cross Language Information Retrieval", as well as automatic system selection, and the experimental analysis.

## Installation

For now, just install the python packages in `requirements.txt`:

```
pip install -r requirements.txt
```

Future versions of this repo will turn `clcomb` into a proper pip-installable python package, but that's further down the roadmap.

## Combination

There are three different post-retrieval evidence combination techniques implemented in this repository:

1. Reciprocal Rank (RR) combination
2. CombMNZ
3. Borda Counts

Each of them have the same footprint (though you can also set technique-specific parameters). For RR Combination, run:

```
python -m clcomb.combination.rr --systems [TREC FILE 1] [TREC FILE 2] ... [TREC FILE N] > [TREC OUTPUT]
```

For CombMNZ, run:

```
python -m clcomb.combination.combmnz --systems [TREC FILE 1] [TREC FILE 2] ... [TREC FILE N] > [TREC OUTPUT]
```

For Borda Count, run:

```
python -m clcomb.combination.borda --systems [TREC FILE 1] [TREC FILE 2] ... [TREC FILE N] > [TREC OUTPUT]
```

This assumes that the system outputs to be combined are in TREC file format, and it generates a TREC formatted file.

## System Selection

To do automatic system selection, you'll need to run the code in `clcomb.selection`.
We have three ways of doing system selection, all described in the paper:

1. Automatic selection, whereby we cluster the systems into `K` clusters, and select the best-performing system from each cluster
2. Stratified sampling selection, whereby we cluster the systems into `K` clusters, and randomly select a system from each cluster
3. Random selection, whereby we randomly sample `N` systems

Like above, the provided utilities are simple command-line utilities.
For automatic selection, run:

```
python -m clcomb.selection.automatic --systems [TREC FILE 1] [TREC FILE 2] [TREC FILE 3] --qrels [QRELS FILE] [--clusters [K]]
```

For stratified sampling selection, run:

```
python -m clcomb.selection.stratified --systems [TREC FILE 1] [TREC FILE 2] [TREC FILE 3] --qrels [QRELS FILE] [--clusters [K]]
```

For random selection, run:

```
python -m clcomb.selection.random --systems [TREC FILE 1] [TREC FILE 2] [TREC FILE 3] --systems [N]
```

## Analysis

`TODO [JOE]: Begin writing/structuring the analysis code.`

## Utilities

The data in this paper was in a specific format, and the provided utilities (`gather_run.sh`, `generate_qrels.sh`) are to normalize that data format.
If you're running this repo on the MATERIAL SCRIPTS system, you can use the utilities in the following way:

**To Create a Single TREC File for a Single System**

```
bash ./utils/create_trec.sh [PATH TO CLIR RUN DIRECTORY] > [OUTPUT TREC FILE]
```

**To Create a Single QREL File from a Build Pack**

```
bash ./utils/create_qrels.py [JUDGEMENTS 1] [JUDGEMENTS 2] ... [JUDGEMENTS N]
```
