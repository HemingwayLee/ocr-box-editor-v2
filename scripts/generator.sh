#!/bin/bash

path=$1
lng=$2

# it needs to be tesseract 4.1.1 or higher version, 4.0.0 does not support wordstrbox
boxfilename=$(echo "$path" | cut -f 1 -d '.')
tesseract $path $boxfilename -l $lng --psm 6 wordstrbox

