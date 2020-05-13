#!/bin/bash

input=$1/*.trec
#~/Research/data/clcomb/eval/
output=$2
#~/Research/data/clcomb/lt/eval_sto/
method=$3
# sto, minmax, rr, borda

mkdir -p $output

cd ~/Research/software/clcomb/clcomb/normalization

for file in $input
do
  base="$(basename $file)"
  echo $base
  python $method.py $file > $output/$base
done
