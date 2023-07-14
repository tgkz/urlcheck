# urlcheck - Check URLs in all the files under specified directory

# Features

- explore specified directory, find .tex file and read it
- If there is any URLs, check the URL is valid, using wget --spider
- If URL is not valid then print the following error messages
In file: <filename>
<linenumber>: <source text the error occured that the URL included>
Error Code: NN URL: <url the error found>
<Error message from wget --spider>
