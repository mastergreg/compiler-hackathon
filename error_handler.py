#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : error_handler.py
# Creation Date : 11-05-2012
# Last Modified : Fri 11 May 2012 05:40:54 PM EEST
# Created By : Greg Liras <gregliras@gmail.com>
#_._._._._._._._._._._._._._._._._._._._._.*/

from sys import stderr
from tree import node

def main():
    eit(0)

if __name__=="__main__":
    main()



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
    '''prints the errors returned by the parser/lexer'''
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
    

if __name__=="__main__":
    exit(0)

