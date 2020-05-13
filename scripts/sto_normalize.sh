#!/bin/bash

INPUT=$1/*.trec
#~/Research/data/clcomb/eval/
OUTPUT=$2
#~/Research/data/clcomb/lt/eval_sto/

mkdir -p $OUTPUT

cd ~/Research/software/clcomb/clcomb/normalization

for file in $INPUT
do
  base="$(basename $file)"
  echo $base
  python sto.py $file > $OUTPUT/$base
done
