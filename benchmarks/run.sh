#!/usr/bin/env bash
set -e
set -u
set -o pipefail

export CC=$(which clang)
export CXX=$(which clang++)
export RUNNER=$1

rm -rf bin/* 
rm -rf output/*

echo "  ---- Building Binary : ${RUNNER} ----  "
cd bin/
CC=$CC CXX=$CXX cmake \
    -DCMAKE_CXX_FLAGS="-w -g -fsanitize=address -fsanitize=leak" \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ../
    
# clang-tidy -checks=* -p bin/ ../src/${RUNNER}.cpp
make -j 2
cd ../

echo "  ---- Running Binary : ${RUNNER} ----  "
bin/${RUNNER} < tests/input.txt
echo "  ---- ${RUNNER} ----  "