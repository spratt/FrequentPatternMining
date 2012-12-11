#!/bin/bash
TIME=`date +%s`
../code/fpgrowth_timing.py ../logs/fpgrowth.timing.${TIME}.txt 1 10 2> /dev/null
