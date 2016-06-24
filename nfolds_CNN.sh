#!/bin/bash
#

if [ $# -lt 2 ]; then
    echo $0: usage: nfolds_CNN.sh model_name nfolds
    exit 1
fi

model_name=$1
nfolds=$2

if [[ $nfolds != ?(-)+([0-9]) ]]; then
  echo $0: usage: nfolds_CNN.sh model_name nfolds
  echo nfolds must be an integer
  exit 1
fi

index=0
for letter in {a..z} ; do
  current_model=$model_name"$letter"
  if [ ! -f ./trained_models/$current_model/"$current_model".sqlite3 ]; then
    ./script_steps.sh $current_model aaaa
  else
    ./script_steps.sh $current_model
  fi

  let index=index+1
  if [ $index -eq $nfolds ]; then
   echo nfold finished successfully
   exit 1
  fi
done
