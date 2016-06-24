#!/bin/sh
#

if [ $# -lt 2 ]; then
    echo $0: usage: nfolds_CNN.sh model_name nfolds
    exit 1
fi

model_name=$1
nfolds=$2

