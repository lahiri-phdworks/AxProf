#!/usr/bin/env bash
set -e
set -u
set -o pipefail

python3 montyhall.py > logs/montyhall.log
python3 schwartz_zippel.py > logs/schwartz_zippel.log
python3 reservior_sampling.py > logs/reservior_sampling.log
python3 zp_hash.py > logs/zp_hash.log
python3 randomized_response.py > logs/randomized_response.log
python3 frievalds.py > logs/frievalds.log   
python3 partition.py > logs/partition.log