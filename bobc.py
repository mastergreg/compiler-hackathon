#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : main.py
# Creation Date : 29-03-2012
# Last Modified : Thu 10 May 2012 07:32:48 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/
from lexer import lexer
from parser import parser
from prules import errors
import readline
from sys import argv,stderr
from tree import node
from getopt import gnu_getopt
from string import replace as sreplace

def find_column(inp,token):
    last_cr = inp.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

def get_error_line_with_color(inp,token):
    last_cr = inp.rfind('\n',0,token.lexpos)
    next_cr = inp.find('\n',token.lexpos)
    if last_cr < 0:
        last_cr = 0
    line = inp[last_cr+1:next_cr]
    for i in range(len(line)):
        if ord(line[i]) == 9:
            continue
        else:
            break
    line = sreplace(line[i:],token.value,'\033[4;32m'+token.value+'\033[0m')
    return line

def print_errors(merrors,data,filename='stdin'):
    '''prints the errors returned by the parser'''
    if merrors:
        for p in merrors:
            text = get_error_line_with_color(data,p)
            pline = p.lineno
            pcolumn = find_column(data,p)
            stderr.write("{0}:{1}:{2}  syntax error: '{3}'\n".format(filename,pline,pcolumn,text,p))
            exit(-1)
        return False
    else:
        return True
    


def main():
    if len(argv) > 1:
        #get command line arguements
        switches,args = gnu_getopt(argv[1:],':o:')
        switches = dict(switches)

        filename = args[0]

        outfile = switches['-o']
        f = open(filename, "r")
        #for line in f:
        data = f.read()
        f.close()
        y = parser.parse(data)
        if print_errors(errors,data,filename):
            f = open(outfile,"w")
            f.write(sreplace(repr(y),'None',''))
            f.close()
    else:
        print "No input given"
        exit(-1)


if __name__=="__main__":
    main()
    exit(0)

