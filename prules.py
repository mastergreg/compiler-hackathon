#!/usr/bin/env python # -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : parserules.py
# Creation Date : 02-04-2012
# Last Modified : Sat 12 May 2012 09:12:40 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/

from tokrules import *
import ply.yacc as yacc
from tree import *
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
    perrors.append(p)
    while 1:
        tok = yacc.token()
        if not tok or tok.value == '}': break
    yacc.restart()


def p_program(p):
    '''
    program  :   def
    '''
    p[0] = TranslationUnit(p[1])

def p_program_2(p):
    '''
    program  :   def program
    '''
    p[0] = p[1].add(p[2])


def p_def_v(p):
    '''
    def     : var_def ';'

    '''
    p[0] = p[1]

def p_def_void(p):
    '''
    def     : Void Id '(' ')' block

    '''
    p[0] = FunctionDefn(Declaration(p[2],'void'),p[5])

def p_def_void_params(p):
    '''
    def     : Void Id '(' formal_params ')' block

    '''
    p[0] = FunctionExpression(FunctionDefn(Declaration(p[2],'void'),p[6]),p[4])

def p_def_ext(p):
    '''
    def     : type Id '(' ')' block
    '''
    p[0] = FunctionDefn(Declaration(p[2],p[1]),p[5])

def p_def_ext_params(p):
    '''
    def     : type Id '(' formal_params ')' block
    '''
    p[0] = FunctionExpression(FunctionDefn(Declaration(p[2],p[1]),p[6]),p[4])


def p_var_def(p):
    '''
    var_def     : type Id
    '''
    p[0] = Declaration(p[2],p[1])
def p_var_def_assign(p):
    '''
    var_def     : type Id ASSIGN expr
    '''
    p[0] = Binop(Declaration(p[2],p[1]),p[4],p[3])


def p_type(p):
    '''
    type    :   simple_type
    '''
    p[0] = p[1]

def p_type_2(p):
    '''
    type    :   simple_type '[' ']' 
    '''
    p[0] = ArrayOf(p[1])
    

def p_simple_type(p):
    '''
    simple_type : Bool
                | Int 
                | Char
    '''
    p[0] = BaseType(p[1].lower())


def p_formal_params(p):
    '''
    formal_params   : type Id rep_formal_params
    '''
    p[0] = ParamList(Declaration(p[2],p[1]))
    p[0].add(p[3])



def p_rep_formal_params_empty(p):
    '''
    rep_formal_params   : empty
    '''
    pass

def p_rep_formal_params(p):
    '''
    rep_formal_params   : ','  type Id rep_formal_params
    '''
    p[0] = ParamList(Declaration(p[3],p[2]))
    p[0].add(p[4])


def p_actual_params(p):
    '''
    actual_params   : expr rep_actual_params
    '''
    p[0] = ArgumentList(p[1])
    p[0].add(p[2])

def p_rep_actual_params_empty(p):
    '''
    rep_actual_params   : empty
    '''
    pass

def p_rep_actual_params(p):
    '''
    rep_actual_params   : ',' expr rep_actual_params
    '''
    p[0] = ArgumentList(p[2])
    p[0].add(p[3])


def p_block(p):
    '''
    block       : '{' '}'
    '''
    pass

def p_block_full(p):
    '''
    block       : '{' stmt_list '}'
    '''
    p[0] = p[2]


def p_stmt_list(p):
    '''
    stmt_list   : stmt 
    '''
    p[0] = Statement(p[1])

def p_stmt_list_2(p):
    '''
    stmt_list   : stmt stmt_list
    '''
    p[0] = StatementList(p[1])
    p[0].add(p[2])

def p_stmt_if(p):
    '''
    stmt    : If '(' expr ')'  stmt
    '''
    p[0] = IfStatement(p[3], p[5])

def p_stmt_ifelse(p):
    '''
    stmt    : If '(' expr ')'  stmt Else stmt
    '''
    p[0] = IfElseStatement(p[3], p[5], p[7])

def p_stmt_for(p):
    '''
    stmt    : For '(' var_def ';' expr ';' stmt ')' stmt
    '''
    p[0] = ForLoop(p[3], p[4], p[5], p[6])

def p_stmt_while(p):
    '''
    stmt    : While '(' expr ')' stmt
    '''
    p[0] = WhileLoop(p[3], p[5])

def p_stmt(p):
    '''
    stmt    : var_def ';'
            | expr ';'
            | block
    '''
    p[0] = p[1]

def p_stmt_del(p):
    '''
    stmt    : Delete expr ';'
    '''
    p[0] = DeleteStatement([2])

def p_stmt_ret(p):
    '''
    stmt    : Ret expr ';'
            | Ret ';'
    '''
    try:
        p[0] = ReturnStatement(p[2])
    except:
        p[0] = ReturnStatement()



def p_expr(p):
    '''
    expr    : Id
    '''
    p[0] = Id(p[1],p.lineno)

def p_expr_2(p):
    '''
     expr    : expr '[' expr ']'
    '''
    p[0] = ArrayExpression(p[1],p[3])

def p_expr_3(p):
    '''
    expr    : Id '(' ')'
    '''
    p[0] = FunctionExpression(Id(p[1],p.lineno),NodeList(NullNode))
    

def p_expr_4(p):
    '''
    expr     : Id '(' actual_params ')'
    '''
    p[0] = FunctionExpression(Id(p[1],p.lineno),p[3])

def p_expr_new(p):
    '''
    expr    : New simple_type '[' expr ']'
    '''
    p[0] = NewStatement(p[2], p[4])

def p_expr_size(p):
    '''
    expr    : Size expr
    '''
    p[0] = SizeStatement(p[2])

def p_expr_atom_int(p):
    '''
    expr    : Const_int
    '''
    p[0] = Const(p[1],BaseType('int'))
    
def p_expr_atom_char(p):
    '''
    expr    : Const_char
    '''
    p[0] = Const(p[1],BaseType('char'))
    
def p_expr_atom_str(p):
    '''
    expr    : Const_str
    '''
    p[0] = Const(p[1],BaseType('str'))

def p_expr_atom_bool(p):
    '''
    expr    : True
            | False
    '''
    p[0] = Const(p[1],BaseType('bool'))


def p_bin_op(p):
    '''
    expr    : expr  ASSIGN expr
    '''
    p[0] = Binop(p[1], p[3], p[2])

def p_bin_op_int(p):
    '''
    expr    : expr  '+'    expr
            | expr  '-'    expr
            | expr  '*'    expr
            | expr  '/'    expr
            | expr  '%'    expr
    '''
    p[0] = Binop(p[1], p[3], p[2])

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
    p[0] = Binop(p[1], p[3], p[2])

def p_un_op(p):
    '''
    expr        : '!' expr %prec UNAR
    '''
    p[0] = Not(p[2])
     
def p_un_op_int(p):
    '''
    expr        : '-' expr %prec UNAR
                | '+' expr %prec UNAR
    '''
    if p[1] == '+':
        p[0] = Positive(p[2])
    else:
        p[0] = Negative(p[2])

