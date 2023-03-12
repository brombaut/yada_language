#!/bin/bash
eval "$(conda shell.bash hook)";
conda activate yada;
# test_files=( "$inputDir"/*txt)
python3 -m pytest "$(dirname "$0")"/test_*.py;