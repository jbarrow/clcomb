#!/bin/bash

input=$1
#~/Research/data/clcomb/eval/
output=$2
#~/Research/data/clcomb/lt/eval_sto/
method=$3
# sto, minmax, rr, borda

mkdir -p $output

for file in $input/*.trec
do
  # clean the blasted trec file
  sed -i '/^$/d' $file
  base="$(basename $file)"
  echo $base
  python -m clcomb.normalization.$method $file > $output/$base
done
