#!/usr/bin/env python # -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : parserules.py
# Creation Date : 02-04-2012
# Last Modified : Fri 11 May 2012 10:01:40 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/

from tokrules import *
import ply.yacc as yacc
from tree import node
from sys import argv
perrors = []



precedence = (  ('nonassoc','If'),
                ('nonassoc','Else'),
                ('nonassoc',','),
                ('right','ASSIGN'),
                ('left','OR'),
                ('left','^'),
                ('left','BINAND'),
                ('left','EQ','NOTEQ'),
                ('left','>','<','LEQ','GEQ'),
                ('left','+','-'),
                ('left','*','/','%'),
                ('nonassoc','UNAR','Size'),
                ('right','[',']','(',')')
            )

start = 'program'


def gen_p_out(title,p,symbol=None,ptype=None):
    children = []
    for i in p[1:]:
        children.append(i)
    r = node(title, {'symbol':symbol,'title':title, 'type':ptype}, children)
    return r


def p_empty(p):
    '''empty :'''
    #p[0] = gen_p_out('empty',p)
    pass


def p_error(p):
    if p:
        yacc.restart()
    else:
        perrors.append(p)


def p_program(p):
    '''
    program  :   def program
             |   def
    '''
    p[0] = gen_p_out('program',p)


def p_def_v(p):
    '''
    def     : var_def ';'

    '''
    p[0] = gen_p_out('def', p, ptype=p[1].type())

def p_def_void(p):
    '''
    def     : Void Id '(' ')' block

    '''
    p[0] = gen_p_out('def', p, ptype='void(void)')

def p_def_void_params(p):
    '''
    def     : Void Id '(' formal_params ')' block

    '''
    p[0] = gen_p_out('def', p, ptype='void')

def p_def_ext(p):
    '''
    def     : type Id '(' ')' block
    '''
    p[0] = gen_p_out('def', p, ptype=p[1].value())

def p_def_ext_params(p):
    '''
    def     : type Id '(' formal_params ')' block
    '''
    p[0] = gen_p_out('def', p, ptype=p[1].value())


def p_var_def(p):
    '''
    var_def     : type Id
                | type Id ASSIGN expr
    '''
    p[0] = gen_p_out('var_def',p, ptype=p[1].value())


def p_type(p):
    '''
    type    :   simple_type
            |   simple_type '[' ']' 
    '''
    p[0] = gen_p_out('type',p,ptype=p[1].type())
    

def p_simple_type(p):
    '''
    simple_type : Bool
                | Int 
                | Char
    '''
    p[0] = gen_p_out('simple_type',p,ptype=p[1])


def p_formal_params(p):
    '''
    formal_params   : type Id rep_formal_params
    '''
    try:
        p[0] = gen_p_out('formal_params',p,ptype=p[1].value()+","+p[3].type())
    except:
        p[0] = gen_p_out('formal_params',p,ptype=p[1].value())



def p_rep_formal_params_empty(p):
    '''
    rep_formal_params   : empty
    '''
    pass

def p_rep_formal_params(p):
    '''
    rep_formal_params   : ','  type Id rep_formal_params
    '''
    p[0] = gen_p_out('formal_params',p)


def p_actual_params(p):
    '''
    actual_params   : expr rep_actual_params
    '''
    p[0] = gen_p_out('actual_params',p)

def p_rep_actual_params_empty(p):
    '''
    rep_actual_params   : empty
    '''
    pass

def p_rep_actual_params(p):
    '''
    rep_actual_params   : ',' expr rep_actual_params
    '''
    p[0] = gen_p_out('params',p)


def p_block(p):
    '''
    block       : '{' '}'
                | '{' stmt_list '}'
    '''
    p[0] = gen_p_out('block',p)


def p_stmt_list(p):
    '''
    stmt_list   : stmt 
                | stmt stmt_list
    '''
    p[0] = gen_p_out('stmt_list',p)

def p_stmt(p):
    '''
    stmt    : var_def ';'
            | If '(' expr ')'  stmt
            | If '(' expr ')'  stmt Else stmt
            | For '(' var_def ';' expr ';' stmt ')' stmt
            | While '(' expr ')' stmt
            | expr ';'
            | block
            | Delete expr ';'
            | Ret expr ';'
            | Ret ';'
    '''
    p[0] = gen_p_out('stmt',p)


def p_expr(p):
    '''
    expr    : Id
            | expr '[' expr ']'
            | Id '(' ')'
            | Id '(' actual_params ')'
            | New simple_type '[' expr ']'
            | Size expr
    '''
    p[0] = gen_p_out('expr',p)

def p_expr_atom(p):
    '''
    expr    : Const_int
            | Const_char
            | Const_str
            | True
            | False
    '''
    p[0] = gen_p_out('expr',p,ptype=p[1])

def p_bin_op(p):
    '''
    expr    : expr  ASSIGN expr
    '''
    p[0] = gen_p_out('binop',p,symbol=p[2])

def p_bin_op_int(p):
    '''
    expr    : expr  '+'    expr
            | expr  '-'    expr
            | expr  '*'    expr
            | expr  '/'    expr
            | expr  '%'    expr
    '''
    p[0] = gen_p_out('binop',p,symbol=p[2], ptype='int')

def p_bin_op_bool(p):
    '''
    expr    : expr  EQ     expr
            | expr  NOTEQ  expr
            | expr  '>'    expr
            | expr  '<'    expr
            | expr  GEQ    expr
            | expr  LEQ    expr
            | expr  BINAND expr
            | expr  OR     expr
            | expr  '^'    expr
    '''
    p[0] = gen_p_out('binop',p,symbol=p[2], ptype='bool')

    

def p_un_op(p):
    '''
    expr        : '!' expr %prec UNAR
    '''
    p[0] = gen_p_out('unop', p, symbol=p[1], ptype='bool')
     

def p_un_op_int(p):
    '''
    expr        : '-' expr %prec UNAR
                | '+' expr %prec UNAR
    '''
    p[0] = gen_p_out('unop',p,symbol=p[1], ptype='int')

