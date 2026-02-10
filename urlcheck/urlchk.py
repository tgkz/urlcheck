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

def fileinit(filetype):
# set regular expression accoridng to the filetype
    global strcomp
    match filetype:
        case "md":
            # expects "(https://URLbody)" in .md files
            strcomp = re.compile(r'\(https?://[^)]*\)')
        case "tex":
            # expects "\url{https://URLbody}" in TeX files
            strcomp = re.compile('\\\\url{.*?}')
        case _:
            # expects "https://URLbody " in .txt normal text files
            strcomp = re.compile(r'https?://\S+')

def geturls(line_image, filetype):
# get urls in a line_image and return urls depending on file types
    global strcomp
    urls = []
    str = strcomp.findall(line_image)
    for s in str:
        match filetype:
            case "tex": 
                url = s.strip('\\\\url{').rstrip('}')  # tex file only
            case "md":
                url = s.strip('(').rstrip(')')  # .md file only
            case _:
                url = s.strip('http').rstrip(' ') # .txt 
                url = 'http' + url
        urls.append(url)
        #print("Adding URL:", url)
    #if (len(urls) > 0):
    #    print("Going to check ", len(urls), " url")
    return urls

def findurls(num, line_image, filetype):
    # find url in line and check url is valid, return number of errors
    global strcomp, line, line_printed

    line = f'{num:05}: '+line_image
    line_printed = False
    errcount = 0    

    urls = geturls(line_image, filetype)
    if (len(urls) > 0):
        #print ("**Found ",len(urls), "url(s) in line:#", num)
        for url in urls:
            print("Checking ", url)
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
    filetype = filename.split('.')[-1] # get file extension like .md
    fileinit(filetype)

    with open(filename, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        linenum = 1
        errors = 0
        for line in lines:
            #print("Line:", linenum, line.rstrip())
            if (len(line) > 0):
                numerr = findurls(linenum, line, filetype)
            linenum = linenum + 1
            errors = errors + numerr
        
        if (errors !=0):
            print (errors, "error found")
        exit(errors)
    
if __name__ == "__main__":
    main()
