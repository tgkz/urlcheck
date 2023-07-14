#!/bin/bash
# urlcheck.sh: check urls for all the files in specified directory
# Usage : urlcheck.sh <directory>
# 
if [ $# -ne 1 ]; then
    echo "Please specify a directory to be checked"
    exit 1
fi
DIR=$1
TMPFILE=/tmp/urlcheck$$.out
find $DIR -name "*.tex" -exec python3 urlchk.py {} \; |tee $TMPFILE
errfiles=`grep error $TMPFILE |wc -l`
errnum=`grep error $TMPFILE |awk 'BEGIN{c=0}/error/{c=c+$1}END{print c}'`
if [ $errnum -gt 0 ]; then
    echo "Total "$errnum" errors found in" $errfiles "files."
fi
rm $TMPFILE
