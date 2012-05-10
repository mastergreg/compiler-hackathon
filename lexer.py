#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : lexer.py
# Creation Date : 21-03-2012
# Last Modified : Thu 10 May 2012 07:32:48 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/

# Build the lexer
from tokrules import *
import ply.lex as lex
from sys import argv
import readline

lexer = lex.lex()
def main():
    global lexer
    if len(argv) > 1:
        f = open(argv[1], "r")
        for line in f:
            lexer.input(line)
            while 1:
                tok = lexer.token()
                if not tok: 
                    break
                #uncomment to print tokens
                #print tok
    else:
        print "No input given"
        exit(-1)

if __name__ == "__main__":
    main()

### Stuff for Parser later on ###

## Precedence rules for the arithmetic operators
#precedence = (
#    ('left','Plus','Minus','RealPlus','RealMinus'),
#    ('left','Mul','Div','RealMul','RealDiv'),
#    ('left','Pow')
#    )
#
## dictionary of names (for storing variables)
#names = { }
#
#
#def p_error(p):
#    print("Syntax error at '%s'" % p.value)
#
#import ply.yacc as yacc
#yacc.yacc()
#
#while 1:
#    try:
#        s = raw_input('test test:')
#    except EOFError:
#        break
#    yacc.parse(s)
