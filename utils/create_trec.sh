#!/bin/bash

# Arguments:
# $1 - Path to run (where the per-query .trec files are output to)

run_path=$1

cat $run_path/*.trec
