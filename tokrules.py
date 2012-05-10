#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : tokrules.py
# Creation Date : 29-03-2012
# Last Modified : Thu 10 May 2012 08:26:12 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/
from sys import argv
terrors = []

reserved = {
'void'      : 't_Void',
'bool'      : 't_Bool',
'int'       : 't_Int',
'char'      : 't_Char',
'size'      : 't_Size',
'new'       : 't_New',
'delete'    : 't_Delete',
'if'        : 't_If',
'else'      : 't_Else',
'for'       : 't_For',
'while'     : 't_While',
'return'    : 't_Ret'
}

literals = [ '+', '-', '*', '/', '(', ')', ';', '!', '<', '>', '^', '%', '{', '}', '[', ']', ',', ':' ]

tokens = [ 'Func', 'BSlash',
'RealPlus', 'RealMinus', 'RealMul', 'RealDiv', 'Pow', 'BINAND', 'OR',
'DomEQ', 'LEQ', 'GEQ', 'EQ', 'NOTEQ', 'ASSIGN',
'Constructor','Const_str','Const_int','Const_float','Const_char', 'Comment', 'ccomment',
'Identifier' ] + list(reserved.values())

# Tokens

t_BINAND         =  r'&&'
t_OR             =  r'\|\|'
t_LEQ            =  r'<='
t_GEQ            =  r'>='
t_EQ             =  r'=='
t_NOTEQ          =  r'!='
t_ASSIGN         =  r':='

t_Const_str      =  r'\"([^\\\n]|(\\.))*?\"'
t_Const_int      =  r'[0-9]+'
t_Const_char     =  r'\'(\\[nrt0\\\"\']|\\x[0-9a-fA-F]{2}|[a-zA-Z])\''
t_ignore_Comment =  r'//.*'
t_ignore         =  " \t"

# Declare the state
states = (
    ('ccomment','exclusive'),
)

def t_ccomment(t):
    r'/\*'
    try:
        if t.lexer.level == 0:
            t.lexer.code_start = t.lexer.lexpos         # Record the starting position
            t.lexer.level = 1                           # Initial brace level
            t.lexer.begin('ccomment')                  # Enter 'ccomment' state
        else:
            t.lexer.level += 1
    except AttributeError:
        t.lexer.code_start = t.lexer.lexpos         # Record the starting position
        t.lexer.level = 1                           # Initial brace level
        t.lexer.begin('ccomment')                  # Enter 'ccomment' state

# Rules for the comment state
def t_ccomment_start(t):
    r'/\*'
    t.lexer.level +=1

def t_ccomment_end(t):
    r'\*/'
    t.lexer.level -=1

    # If closing brace, return the comment fragment
    if t.lexer.level == 0:
         t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1]
         t.type = "ccomment"
         t.lexer.lineno += t.value.count('\n')
         t.lexer.begin('INITIAL')
         pass
         #return t

def t_ccomment_anydata(t):
    r'([^*//]+|\*|\(|\))'
    t.lexer.lineno += t.value.count("\n")
    pass

def t_ccomment_lparen(t):
    r'\/'
    pass

def t_ccomment_rparen(t):
    r'\/'
    pass


def t_ccomment_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Ignored characters (whitespace)
t_ccomment_ignore = " \t"

# For bad characters, we just skip over it
def t_ccomment_error(t):
    t.lexer.skip(1)

def t_Reserved(t):
    r'[a-z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'Identifier')    # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    terrors.append(t)
    t.lexer.skip(1)
