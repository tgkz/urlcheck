#!/bin/bash
# urlcheck.sh: check urls for set of tex files
# NOTE: please set you own directory to DIR :
DIR=$HOME/Projects/LFJapan/Traning/LFCW/linuxfoundation-jp/LFS301/LFS301/CHAPS/
DIR=$HOME/Projects/LFJapan/Traning/LFCW/linuxfoundation-jp/LFJP-LFD259/LFD259-JP/CHAPS
DIR=$HOME/Projects/LFJapan/Traning/LFCW/linuxfoundation-jp/LFJP-LFD259/LFD459-JP/CHAPS
if [ $# -ne 1 ]; then
    echo "Please specify a directory to be checked"
    exit 1
fi
DIR=$1
#for i in $DIR/*/*.tex; do python3 urlck.py $i; done |tee temp.out
find $DIR -name "*.tex" -exec python3 urlck.py {} \; |tee temp.out
errfiles=`grep error temp.out|wc -l`
errnum=`grep error temp.out|awk 'BEGIN{c=0}/error/{c=c+$1}END{print c}'`
if [ $errnum -gt 0 ]; then
    echo "Total "$errnum" errors found in" $errfiles "files."
fi
rm temp.out

