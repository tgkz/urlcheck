#!usr/bin/env python3
# -*- coding: utf-8 -*-
# Usage: urlck filename
# urlck: Find urls in a specified file and check whether it's valid
# This version is expecting .tex files thus we exepct "\url{http://URL}"

import re, sys
# import regex for the replacement of re for analysing UTF-8
import subprocess

filename = ""
filename_printed = False
def printfilename():
    global filename, filename_printed
    if (filename_printed == False):
        print("In file:", filename)
        filename_printed = True
    return

line=""
line_printed=False
def print_line():
    global line, line_printed
    if (line_printed == False):
        print(line, end="")
        line_printed = True
    return
 
def checkurl(url):
    commandline = ["wget", "--spider", "--wait", "1", "-nv", "--tries=1", "--timeout=3"]
    commandline.append(url)
    #print (commandline)
    code = subprocess.run(commandline, capture_output=True, text=True)
    if (code.returncode != 0):
        printfilename()
        print_line()
        print("Error Code:", code.returncode, "URL:", url)
        print(code.stderr, end="")
    return code.returncode

# strcomp: regular expression for specific source format 
strcomp = re.compile('\\\\url{.*?}')  # expects "\url{https://URLbody}" in TeX files

def findurls(num, line_image):
    # find url in line and check url is valid, return number of errors
    global strcomp, line
    str = strcomp.findall(line_image)
    line = f'{num:06}: '+line_image
    line_printed = False
    errcount = 0    
    if (len(str) > 0):
        #print ("**FIND ",len(str), " pieces in line:#", num)
        for w in str:
            url = w.strip('\\\\url{').rstrip('}')
            cd = checkurl(url)
            if (cd != 0):
                errcount = errcount + 1
    return errcount  # return # of errors

def main():
    global filename, line_printed
    args = sys.argv
    if (len(args) <= 1):
        print("Please specifiy filename")
        sys.exit(-1)

    filename = sys.argv[1]
    with open(filename, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        linenum = 1
        errors = 0
        for line in lines:
            line_printed = False
            #print("Line:", linenum, line.rstrip())
            numerr = findurls(linenum, line)
            linenum = linenum + 1
            errors = errors + numerr
        
        if (errors !=0):
            print (errors, "error found")
        exit(errors)
    
if __name__ == "__main__":
    main()
