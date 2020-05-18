#!/bin/bash

language=$1
metric="manual"

eval=~/Research/data/clcomb/${language}/eval_sto/
eval_qrels=paper/qrels/${language}/eval.qrels

output=~/Research/models/clcomb/lt/

trec_eval=~/Software/trec_eval-9.0.7/trec_eval

# create the directories where we'll be saving the output
mkdir -p ${output}/${metric}/combined

# perform system combination on the eval results
systems=$(sed 's/dev_sto/eval_sto/g ; :a;N;$!ba;s/\n/ /g ; s/dev_sto/eval_sto/g' paper/manual/${language}.txt)
echo $systems
python -m clcomb.combination.rr --systems $systems > ${output}/${metric}/combined/manual.trec

# output the MAP scores for the eval results
$trec_eval -c $eval_qrels ${output}/${metric}/combined/manual.trec | grep ^map | awk '{ print $3 }'
