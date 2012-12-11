#!/bin/bash
TIME=`date +%s`
../code/eclat_timing.py ../logs/eclat.timing.${TIME}.txt 1 10 2> /dev/null
