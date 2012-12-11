#!/bin/bash
TIME=`date +%s`
../code/timing.py 1 10 >> ../logs/timing.${TIME}.txt

