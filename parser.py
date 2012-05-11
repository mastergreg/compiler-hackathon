#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : parser.py
# Creation Date : 21-03-2012
# Last Modified : Fri 11 May 2012 11:22:37 AM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/

from tokrules import tokens
from prules import *
import ply.yacc as yacc

parser = yacc.yacc()
