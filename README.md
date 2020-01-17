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

`TODO [JOE]: Make the system selection code as usable as the evidence combination code, then document it here.`
