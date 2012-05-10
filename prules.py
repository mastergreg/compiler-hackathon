#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : parserules.py
# Creation Date : 02-04-2012
# Last Modified : Fri 11 May 2012 01:23:07 AM EEST
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
                ('nonassoc','[',']','(',')')
            )

start = 'program'


def gen_p_out(ptype,p,symbol=None):
    #r = 'nili'
    #try:
    #    for i in p:
    #        if type(i) == str:
    #            try:
    #                r.add(node(i,{'name':i}))
    #            except AttributeError:
    #                r = node(p[0],{'name':p[0]})
    #            print i,r
    #except TypeError:
    #    return None

    children = []
    for i in p[1:]:
        children.append(i)
    return node(ptype, {'symbol':symbol,'title':ptype}, children)


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


def p_def(p):
    '''
    def     : var_def ';'
            | func_def
    '''
    p[0] = gen_p_out('def',p)


def p_type(p):
    '''
    type    :   simple_type
            |   simple_type '[' ']'
    '''
    p[0] = gen_p_out('type',p)
    #pass
    


def p_ret_type(p):
    '''
    ret_type    : Void
                | type
    '''
    pass

def p_simple_type(p):
    '''
    simple_type : Bool
                | Int 
                | Char
    '''
    pass    

def p_var_def(p):
    '''
    var_def     : type Id
                | type Id ASSIGN expr
    '''
    pass

def p_func_def(p):
    '''
    func_def    : ret_type Id '(' ')' block
                | ret_type Id '(' formal_params ')' block
    '''
    pass

def p_formal_params(p):
    '''
    formal_params   : type Id rep_formal_params
    '''
    pass

def p_rep_formal_params(p):
    '''
    rep_formal_params   : empty
                        | ','  type Id rep_formal_params
    '''
    pass

def p_actual_params(p):
    '''
    actual_params   : expr rep_actual_params
    '''
    pass

def p_rep_actual_params(p):
    '''
    rep_actual_params   : empty
                        | ',' expr rep_actual_params
    '''
    pass


def p_block(p):
    '''
    block       : '{' '}'
                | '{' stmt_list '}'
    '''
    pass


def p_stmtm_list(p):
    '''
    stmt_list   : stmt ';'
                | stmt ';' stmt_list
    '''
    pass

def p_stmt(p):
    '''
    stmt    : var_def
            | If '(' expr ')'  stmt
            | If '(' expr ')'  stmt Else stmt
            | For '(' var_def ';' expr ';' stmt ')' stmt
            | While '(' expr ')' stmt
            | expr
            | block
            | Delete Id
            | Ret expr
    '''
    pass


def p_expr_atom(p):
    '''
    expr_atom   : lval 
                | Size expr_atom
                | New type '[' expr ']'
                | Const_int
                | Const_char
                | Const_str
                | True
                | False
                | Id '(' ')'
                | Id '(' actual_params ')'
                | Id ASSIGN expr
    '''

def p_expr(p):
    '''
    expr    : expr_atom 
            | expr  '+'    expr
            | expr  '-'    expr
            | expr  '*'    expr
            | expr  '/'    expr
            | expr  '%'    expr
            | expr  EQ     expr
            | expr  NOTEQ  expr
            | expr  '>'    expr
            | expr  '<'    expr
            | expr  GEQ    expr
            | expr  LEQ    expr
            | expr  BINAND expr
            | expr  OR     expr
            | expr  '^'    expr

    '''
    pass
    

def p_un_op(p):
    '''
    expr        : '!' expr %prec UNAR
                | '-' expr %prec UNAR
                | '+' expr %prec UNAR
    '''
    pass

def p_lval(p):
    '''
    lval    : Id
            | Id '[' expr ']'
    '''
    pass

    
