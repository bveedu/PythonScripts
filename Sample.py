#!/usr/bin/python

# import modules used here -- sys is a very standard one
import sys
import os
import re
import Sample
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


# Gather our code in a main() function
def main():
    ## sys module
    print ('Hello there', sys.argv[0])
 
    '''  Calling a function calculate()
    '''
    print ("calculate",calculate(1,2))
    
    ## Calling a function in imported module
    print ("calculate",Sample.calculate(1,2))
  
    ## os module  
    print(os.getenv('CLASSPATH'))

    ## Regular expressions
    print(re.compile('ram3*').match('ram33').pos)
    match= re.search(r'iii', 'piiig')
    if match:
        print (match.group())
   
    ##lists
    colors = ['red', 'blue', 'green']
    ##sort
    colors.sort()
    print (colors[0])    ## red
    print(len(colors))
    print(colors)
    squares = [1, 4, 9, 16]

    ## for loop
    sum = 0
    for num in squares:
        sum += num
    print (sum)  ## 30

    ##While loop
    i=0
    while i<10:
        i=i+3
        print(i)
    nums = [1, 2, 3, 4]

    ## List comprehensions
    squares = [ n * n for n in nums ]   ## [1, 4, 9, 16]
    print(squares)
    
    ## Tuple
    tuple = (1, 2, 'hi')
    print (tuple[2] )  ## 2

    # Echo the contents of a file
    f = open('Sample.py', 'rU')
    for line in f:   ## iterates over the lines of the file
        print(line,)    ## trailing , so print does not add an end-of-line char
                   ## since 'line' already includes the end-of line.
    f.close()

    ## Dictionary
    dict = {'c':'ram'}
    dict['a'] = 'alpha'
    dict['g'] = 'gamma'
    dict['o'] = 'omega'

    print (dict )
    print (dict.keys())

    ## Exceptions
    try:
        ## Either of these two lines could throw an IOError, say
        ## if the file does not exist or the read() encounters a low level error.
        f = open('Sample.p', 'rU')
        text = f.read()
        f.close()
    except IOError:
        ## Control jumps directly to here if any of the above lines throws IOError.
        sys.stderr.write('problem reading file')

    ## Using urllib
    wget('http://www.google.com')

# Functions
def calculate(num1,num2):
    return num1+num2
## Given a url, try to retrieve it. If it's text/html,
## print its base url and its text.
def wget(url):
    try:
        req = Request(url)
        response = urlopen(req)
        print(response)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        print('Every thing is fine ')

# Standard boilerplate to call the main() function to begin
# the program.
if __name__=='__main__':
    main()
