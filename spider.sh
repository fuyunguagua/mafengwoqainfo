#!/usr/bin/env bash
date
python3 ./qa/run.py
#nohup python3 ./qa/run.py > /dev/null 2>&1 &
echo "Start spider success!"