#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : tokrules.py
# Creation Date : 29-03-2012
# Last Modified : Thu 10 May 2012 07:32:13 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/
from sys import argv

reserved = {
'void'      : 'Void',
'bool'      : 'Bool',
'int'       : 'Int',
'char'      : 'Char',
'size'      : 'Size',
'new'       : 'New',
'delete'    : 'Delete',
'if'        : 'If',
'else'      : 'Else',
'for'       : 'For',
'while'     : 'While',
'return'    : 'Ret'
}

literals = [ '+', '-', '*', '/', '(', ')', ';', '!', '<', '>', '^', '%', '[', ']', ',', ':' ]

tokens = [ 'Func', 'BSlash',
'RealPlus', 'RealMinus', 'RealMul', 'RealDiv', 'Pow', 'BINAND', 'OR',
'DomEQ', 'LEQ', 'GEQ', 'EQ', 'NOTEQ', 'ASSIGN',
'Constructor','Const_str','Const_int','Const_float','Const_char', 'Comment', 'MlComment',
'Identifier' ] + list(reserved.values())

# Tokens

t_BINAND         =  r'&&'
t_OR             =  r'\|\|'
t_DomEQ          =  r'<>'
t_LEQ            =  r'<='
t_GEQ            =  r'>='
t_EQ             =  r'=='
t_NOTEQ          =  r'!='
t_ASSIGN         =  r':='
t_Const_str      =  r'\"([^\\\n]|(\\.))*?\"'
t_Const_int      =  r'[0-9]+'
t_Const_float    =  r'[0-9]+\.?[0-9]+([eE][+-]?[0-9]+)?'
t_Const_char     =  r'\'(\\[nrt0\\\"\']|\\x[0-9a-fA-F]{2}|[^\'\"\\])\''
t_ignore_Comment =  r'--.*'
t_ignore         =  " \t"

# Declare the state
states = (
    ('mlcomment','exclusive'),
)

def t_mlcomment(t):
    r'\(\*'
    try:
        if t.lexer.level == 0:
            t.lexer.code_start = t.lexer.lexpos         # Record the starting position
            t.lexer.level = 1                           # Initial brace level
            t.lexer.begin('mlcomment')                  # Enter 'mlcomment' state
        else:
            t.lexer.level += 1
    except AttributeError:
        t.lexer.code_start = t.lexer.lexpos         # Record the starting position
        t.lexer.level = 1                           # Initial brace level
        t.lexer.begin('mlcomment')                  # Enter 'mlcomment' state

# Rules for the comment state
def t_mlcomment_start(t):
    r'\(\*'
    t.lexer.level +=1

def t_mlcomment_end(t):
    r'\*\)'
    t.lexer.level -=1

    # If closing brace, return the comment fragment
    if t.lexer.level == 0:
         t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1]
         t.type = "ccomment"
         t.lexer.lineno += t.value.count('\n')
         t.lexer.begin('INITIAL')
         pass
         #return t

def t_mlcomment_anydata(t):
    r'([^*()]+|\*|\(|\))'
    t.lexer.lineno += t.value.count("\n")
    pass

def t_mlcomment_lparen(t):
    r'\('
    pass

def t_mlcomment_rparen(t):
    r'\)'
    pass


def t_mlcomment_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Ignored characters (whitespace)
t_mlcomment_ignore = " \t"

# For bad characters, we just skip over it
def t_mlcomment_error(t):
    t.lexer.skip(1)

def t_Reserved(t):
    r'[a-z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'Identifier')    # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    if len(argv) > 1:
        fname = argv[1]
    else:
        fname = "stdin"
    print("%s:%s:%s #> Illegal character '%s'" % (fname, t.lexer.lineno, t.lexpos, t.value[0]))
    t.lexer.skip(1)
