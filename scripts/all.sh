#!/bin/bash

language=$1
metric="all"

eval=~/Research/data/clcomb/${language}/eval_sto/
eval_qrels=paper/qrels/${language}/eval.qrels

output=~/Research/models/clcomb/lt/

trec_eval=~/Software/trec_eval-9.0.7/trec_eval

# create the directories where we'll be saving the output
mkdir -p ${output}/${metric}/clusters ${output}/${metric}/combined

# perform system combination on the eval results
python -m clcomb.combination.combmnz --systems $eval/*.trec > ${output}/${metric}/combined/all.trec

# output the MAP scores for the eval results
$trec_eval -c $eval_qrels ${output}/${metric}/combined/all.trec | grep ^map | awk '{ print $3 }'
