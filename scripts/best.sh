#!/bin/bash

metric="best"

language=$1
# sw, so, lt

dev=~/Research/data/clcomb/${language}/dev_sto/
eval=~/Research/data/clcomb/${language}/eval_sto/

dev_qrels=paper/qrels/${language}/dev.qrels
eval_qrels=paper/qrels/${language}/eval.qrels

output=~/Research/models/clcomb/${language}/

trec_eval=~/Software/trec_eval-9.0.7/trec_eval

# create the directories where we'll be saving the output
mkdir -p ${output}/${metric}/model ${output}/${metric}/clusters ${output}/${metric}/combined

# perform the clustered selection on the scores
python -m clcomb.selection.top_selection \
  --systems $dev/*.trec \
  --qrels $dev_qrels \
  --K {20..100..10} \
  --output-dir ${output}/${metric}/clusters

# perform system combination on the eval results
for i in {20..100..10}
do
  #systems=$(sed ':a;N;$!ba;s/\n/ /g ; s/dev_sto/eval_sto/g' results/lt/da_best_${i}_1.txt)
  systems=$(sed 's/dev_sto/eval_sto/g ; :a;N;$!ba;s/\n/ /g ; s/dev_sto/eval_sto/g' ${output}/${metric}/clusters/top_${i}.txt)
  echo $systems
  python -m clcomb.combination.combmnz --systems $systems > ${output}/${metric}/combined/top_$i.trec
done

# output the MAP scores for the eval results
for i in {20..100..10}
do
  $trec_eval -c $eval_qrels ${output}/${metric}/combined/top_${i}.trec | grep ^map | awk '{ print $3 }'
done
