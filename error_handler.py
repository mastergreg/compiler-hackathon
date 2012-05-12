#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : error_handler.py
# Creation Date : 11-05-2012
# Last Modified : Sat 12 May 2012 01:32:32 PM EEST
# Created By : Greg Liras <gregliras@gmail.com>
#_._._._._._._._._._._._._._._._._._._._._.*/

from sys import stderr
from tree import node
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
    line = line.strip()
    val =  token.value.split()[0]
    line = sreplace(line,val,'\033[1;31m'+val+'\033[0m')
    return line

def print_errors(merrors,data,filename='stdin'):
    '''prints the errors returned by the parser/lexer'''
    if merrors:
        for p in merrors:
            text = get_error_line_with_color(data,p)
            pline = p.lineno
            pcolumn = find_column(data,p)
            stderr.write("{0}:{1}:{2}  error: '{3}'\n".format(filename,pline,pcolumn,text,p))
        return False
    else:
        return True
    

if __name__=="__main__":
    exit(0)

