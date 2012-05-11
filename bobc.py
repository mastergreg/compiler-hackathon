#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : bobc.py
# Creation Date : 29-03-2012
# Last Modified : Fri 11 May 2012 07:11:09 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/
from lexer import lexer
from parser import parser
from prules import perrors
from tokrules import terrors

from sys import argv
from getopt import gnu_getopt
from string import replace as sreplace

from error_handler import find_column, get_error_line_with_color, print_errors
    
def main():
    if len(argv) > 1:
        #get command line arguements
        switches = {'-o':'a.xml'}
        setswitches,args = gnu_getopt(argv[1:],':o:')
        setswitches = dict(setswitches)

        for i in setswitches.keys():
            switches[i] = setswitches[i]

        filename = args[0]

        outfile = switches['-o']
        f = open(filename, "r")
        #for line in f:
        data = f.read()
        f.close()
        y = parser.parse(data)
        if print_errors(perrors,data,filename) and print_errors(terrors,data,filename):
            f = open(outfile,"w")
            f.write(repr(y))
            #f.write(sreplace(repr(y),'None',''))
            f.close()
    else:
        print "No input given"
        exit(-1)


if __name__=="__main__":
    main()
    exit(0)

