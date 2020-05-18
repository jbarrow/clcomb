#!/bin/bash

language=$1
# lt, so, sw
metric="random"

eval=~/Research/data/clcomb/${language}/eval_sto/
eval_qrels=paper/qrels/${language}/eval.qrels


output=~/Research/models/clcomb/${language}/

trec_eval=~/Software/trec_eval-9.0.7/trec_eval

# create the directories where we'll be saving the output
mkdir -p ${output}/${metric}/clusters ${output}/${metric}/combined

for i in {20..100..10}
do
  for j in {1..10}
  do
    # perform the random selection on the scores
    python -m clcomb.selection.random_selection \
      --systems $eval/*.trec --N $i > ${output}/${metric}/clusters/${i}_${j}.txt
  done
done

# perform system combination on the eval results
for i in {20..100..10}
do
  for j in {1..10}
  do
    #systems=$(sed ':a;N;$!ba;s/\n/ /g ; s/dev_sto/eval_sto/g' results/lt/da_best_${i}_1.txt)
    systems=$(sed ':a;N;$!ba;s/\n/ /g' ${output}/${metric}/clusters/${i}_${j}.txt)
    echo $systems
    python -m clcomb.combination.combmnz --systems $systems > ${output}/${metric}/combined/${i}_${j}.trec
  done
done

# output the MAP scores for the eval results
for i in {20..100..10}
do
  echo "${language} - ${i} systems"
  for j in {1..10}
  do
    $trec_eval -c $eval_qrels ${output}/${metric}/combined/${i}_${j}.trec | grep ^map | awk '{ print $3 }'
  done
done
