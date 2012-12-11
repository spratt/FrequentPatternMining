#!/bin/bash
TIME=`date +%s`
../code/apriori_timing.py ../logs/apriori.timing.${TIME}.txt 1 10 2> /dev/null

