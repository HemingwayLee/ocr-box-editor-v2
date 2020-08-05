#!/bin/bash

path=$1
lng=$2

boxfilename=$(echo "$path" | cut -f 1 -d '.')
tesseract $path $boxfilename -l $lng --psm 6 wordstrbox

