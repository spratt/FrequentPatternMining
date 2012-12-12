#!/bin/bash
for f in `ls *.dot`; do
	ext="${f##*.}"
	file="${f%.*}"
	dot -Tpng $f -o $file.png
done
