#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : parser.py
# Creation Date : 21-03-2012
# Last Modified : Thu 10 May 2012 07:32:48 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/

# Build the lexer
from tokrules import tokens
from prules import *
import ply.yacc as yacc

#def p_error(p):
#    print("Syntax error at '%s'" % p.value)

parser = yacc.yacc()

if __name__ == "__main__":
    main()

