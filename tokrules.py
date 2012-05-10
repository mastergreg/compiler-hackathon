#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : tokrules.py
# Creation Date : 29-03-2012
# Last Modified : Fri 11 May 2012 12:09:34 AM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/
from sys import argv
terrors = []

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
'true'      : 'True',
'false'     : 'False',
'return'    : 'Ret'
}

literals = [ '+', '-', '*', '/', '(', ')', ';', '!', '<', '>', '^', '%', '{', '}', '[', ']', ',', ':' ]

tokens = [ 'BINAND', 'OR', 'LEQ', 'GEQ', 'EQ', 'NOTEQ', 'ASSIGN',
'Const_str','Const_int','Const_char', 'Comment', 'ccomment',
'Id' ] + list(reserved.values())

# Tokens

t_BINAND         =  r'&&'
t_OR             =  r'\|\|'
t_LEQ            =  r'<='
t_GEQ            =  r'>='
t_EQ             =  r'=='
t_NOTEQ          =  r'!='
t_ASSIGN         =  r':='

t_Const_str      =  r'\"([^\\\n]|(\\.))*?\"'
#t_Const_str      =  r'[a-zA-Z_]?\"(\\.|[^\\"])*\"'
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
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'Id')    # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    terrors.append(t)
    t.lexer.skip(1)
