#!/bin/bash

folder=$1
tmp_folder=$2
mkdir -p $folder

#node='(10, 20)'
#multi='1'
#cost='(1, 10)'
#seed='0'

node=$3
multi=$4
cost=$5
seed=$6

tau_1=("0" "0.2" "0.4" "0.6" "0.8" "1.0")
tau_2=("0" "0.2" "0.4" "0.6" "0.8" "1.0")
tau_3=("0" "0.1" "0.2" "0.3" "0.4" "0.5")
agents=("2" "5" "10" "15" "20")

database=$1/database.csv

echo "name, agent, tau_1, tau_2, tau_3" > $database

i=-1
for agent in ${agents[@]}; do
    for t1 in ${tau_1[@]}; do
        for t2 in ${tau_2[@]}; do
            for t3 in ${tau_3[@]}; do
                i=$((i+1))
                if [ $i -eq 0 ]; then
                    continue
                fi
                echo "simple$i, $agent, $t1, $t2, $t3" >> $database
                cat $tmp_folder/simple_agent_template.py \
                    | sed "s/{NODE}/$node/" \
                    | sed "s/{COST_MULTIPLIER}/$multi/" \
                    | sed "s/{COST}/$cost/" \
                    | sed "s/{SEED}/$seed/" \
                    | sed "s/{TAU_1}/$t1/" \
                    | sed "s/{TAU_2}/$t2/" \
                    | sed "s/{TAU_3}/$t3/" \
                    | sed "s/{AGENT}/$agent/" >> $folder/simple_agent_$i.py
            done
        done
    done
done

i=0
for agent in ${agents[@]}; do
    echo "random$i, $agent,,," >> $database
    cat $tmp_folder/random_agent_template.py \
        | sed "s/{NODE}/$node/" \
        | sed "s/{COST_MULTIPLIER}/$multi/" \
        | sed "s/{COST}/$cost/" \
        | sed "s/{SEED}/$seed/" \
        | sed "s/{AGENT}/$agent/" >> $folder/random_agent_$i.py
    i=$((i+1))
done
