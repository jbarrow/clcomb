#!/bin/bash

metric=$1
# cognitive_diversity, pearson, kendall, spearman, jaccard

dev=~/Research/data/clcomb/lt/dev_sto/
eval=~/Research/data/clcomb/lt/eval_sto/

eval_qrels=paper/eval.qrels
dev_qrels=paper/devanal.qrels

output=~/Research/models/clcomb/lt/

trec_eval=~/Software/trec_eval-9.0.7/trec_eval

# create the directories where we'll be saving the output
mkdir -p ${output}/${metric}/model ${output}/${metric}/clusters ${output}/${metric}/combined

# compute the pairwise similarity scores
python -m clcomb.selection.similarity \
  --systems $dev/*.trec \
  --join intersection \
  --metric $metric \
  --output-dir ${output}/${metric}/model

# perform the clustered selection on the scores
python -m clcomb.selection.clustered_selection \
  --systems $dev/*.trec \
  --qrels $dev_qrels \
  --sample best \
  --K {1..15} \
  --comparison-model ${output}/${metric}/model \
  --output-dir ${output}/${metric}/clusters

# perform system combination on the eval results
for i in {1..15}
do
  #systems=$(sed ':a;N;$!ba;s/\n/ /g ; s/dev_sto/eval_sto/g' results/lt/da_best_${i}_1.txt)
  systems=$(sed 's/dev_sto/eval_sto/g ; :a;N;$!ba;s/\n/ /g ; s/dev_sto/eval_sto/g' ${output}/${metric}/clusters/da_best_${i}_1.txt)
  echo $systems
  python -m clcomb.combination.rr --systems $systems > ${output}/${metric}/combined/da_comb_$i.trec
done

# output the MAP scores for the eval results
for i in {1..15}
do
  $trec_eval -c $eval_qrels ${output}/${metric}/combined/da_comb_${i}.trec | grep ^map | awk '{ print $3 }'
done
