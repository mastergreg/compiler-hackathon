#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : parserules.py
# Creation Date : 02-04-2012
# Last Modified : Thu 10 May 2012 07:32:48 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/

from tokrules import *
import ply.yacc as yacc
from tree import node
from sys import argv
errors = []

precedence = (
        ('nonassoc', 'Let', 'In'),
        ('left', ';'),
        ('nonassoc', 'If', 'Then'),
        ('nonassoc', 'Else'),
        ('nonassoc', 'ASSIGN'),
        ('left', 'OR'),
        ('left', 'BINAND'),
        ('nonassoc', '=', 'EQ', 'NOTEQ',  'DomEQ','<', '>', 'LEQ', 'GEQ'),    # Comparisons
        ('left', '+', '-', 'RealPlus', 'RealMinus' ),                   # + -
        ('left', '*', '/', 'RealMul', 'RealDiv', 'Mod'),                # * /
        ('right', 'Pow'),
        ('right', 'UPLUS', 'UMINUS', 'URPLUS', 'URMINUS', 'UNOT', 'Delete'),                                            # Unary Ops
        ('nonassoc','EXPR_FUNC'),
        ('nonassoc', 'UBANG'),
        ('nonassoc', '[', ']'),
        ('nonassoc', 'New')
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
    if p==None:
        yacc.restart()
    else:
        errors.append(p)

def p_program(p):
    '''
    program  :   letdef program
             |   typedef program
    '''
    p[0] = gen_p_out('program',p)
    
def p_program_empty(p):
    '''
    program  :   empty
    '''
    pass

def p_letdef(p):
    '''
    letdef   :   Let def repdef
             |   Let Rec def repdef
    '''
    p[0] = gen_p_out('letdef',p)

def p_repdef(p):
    '''
    repdef   :   And def repdef
    '''
    p[0] = gen_p_out('repdef',p)

def p_repdef_empty(p):
    '''
    repdef   :   empty
    '''
    pass

def p_def(p):
    '''
    def      :   Identifier reppar '=' expr
             |   Identifier reppar ':' type '=' expr
             |   Mutable Identifier
             |   Mutable Identifier ':' type
             |   Mutable Identifier '[' expr repexpr ']'
             |   Mutable Identifier '[' expr repexpr ']' ':' type
    '''
    p[0] = gen_p_out('def',p)

def p_reppar(p):
    '''
    reppar   :   par reppar
    '''
    p[0] = gen_p_out('reppar',p)

def p_reppar_empty(p):
    '''
    reppar   :   empty
    '''
    pass

def p_par(p):
    '''
    par      :   Identifier
             |   '(' Identifier ':' type ')'
    '''
    p[0] = gen_p_out('par',p)

def p_repexpr(p):
    '''
    repexpr  :   ',' expr repexpr
    '''
    p[0] = gen_p_out('repexpr',p)

def p_repexpr_empty(p):
    '''
    repexpr  :   empty
    '''
    pass

def p_typedef(p):
    '''
    typedef  :   Type tdef reptdef
    '''
    p[0] = gen_p_out('typedef',p)

def p_reptdef(p):
    '''
    reptdef  :   And tdef reptdef
    '''
    p[0] = gen_p_out('repdef',p)

def p_reptdef_empty(p):
    '''
    reptdef  :   empty
    '''
    pass

def p_tdef(p):
    '''
    tdef     :   Identifier '=' constr repconstr
    '''
    p[0] = gen_p_out('tdef',p)

def p_repconstr(p):
    '''
    repconstr    :   '|' constr repconstr
    '''
    p[0] = gen_p_out('repconstr',p)

def p_repconstr_empty(p):
    '''
    repconstr    :   empty 
    '''
    pass

def p_constr(p):
    '''
    constr   :   Constructor
             |   Constructor Of type reptype
    '''
    p[0] = gen_p_out('constr',p)

def p_reptype(p):
    '''
    reptype  :   type reptype
    '''
    p[0] = gen_p_out('reptype',p)

def p_reptype_empty(p):
    '''
    reptype  :   empty
    '''
    pass


def p_repstar(p):
    '''
    repstar  :   ',' '*' repstar
    '''
    p[0] = gen_p_out('repstar',p)

def p_repstar_empty(p):
    '''
    repstar  :   empty
    '''
    pass

def p_type_atom(p):
    '''
    type_atom   :   Unit
                |   Int
                |   Char
                |   Bool
                |   Float
                |   '(' type ')'
                |   Array
                |   Array '[' '*' repstar ']' Of type_atom
                |   Identifier
    '''
    p[0] = gen_p_out('type_atom',p)
#|   FIXME:
#|   Array '[' '*' repstar ']' Of type_atom not sure about this one
#|   Array '[' '*' repstar ']' Of type not sure about this one

def p_type_fun(p):
    '''
    type_fun    :   type_atom
                |   type_atom Func type_fun
    '''
    p[0] = gen_p_out('type_fun',p)


def p_type(p):
    '''
    type     :   type_fun
             |   type Ref
    '''
    p[0] = gen_p_out('type',p)



def p_expr_atom(p):
    '''
    expr_atom   :   Const_int       
                |   Const_float     
                |   Const_char      
                |   Const_str       
                |   True            
                |   False           
                |   '(' ')'         
                |   '(' expr ')'    
                |   Identifier
                |   Constructor
                |   Identifier '[' expr repexpr ']'
                |   expr_bang
    '''
    p[0] = gen_p_out('expr_atom',p)

def p_expplus(p):
    '''
    expplus  :   expr_atom
             |   expr_atom expplus
    '''
    p[0] = gen_p_out('expplus',p)

def p_expr(p):
    '''
    expr     :   Identifier expplus %prec EXPR_FUNC
             |   Constructor expplus
             |   expr_atom
             |   expr '+' expr
             |   expr '-' expr
             |   expr '*' expr
             |   expr '/' expr
             |   expr RealPlus expr
             |   expr RealMinus expr
             |   expr RealMul expr
             |   expr RealDiv expr
             |   expr Mod expr
             |   expr Pow expr
             |   expr '=' expr
             |   expr '>' expr
             |   expr '<' expr
             |   expr DomEQ expr
             |   expr LEQ expr
             |   expr GEQ expr
             |   expr EQ expr
             |   expr NOTEQ expr
             |   Dim Identifier
             |   Dim Const_int Identifier
             |   expr BINAND expr
             |   expr OR expr
             |   expr ';' expr
             |   expr ASSIGN expr
             |   New type
             |   Delete expr
             |   letdef In expr
             |   Begin expr End
             |   If expr Then expr
             |   If expr Then expr Else expr
             |   While expr Do expr Done
             |   For Identifier '=' expr To expr Do expr Done
             |   For Identifier '=' expr Downto expr Do expr Done
             |   Match expr With clause repclause End

    '''
    if len(p) == 4:
        try:
            p[0] = gen_p_out('bin_expr',p,symbol=p[2].symbol())
        except:
            p[0] = gen_p_out('bin_expr',p,symbol=p[2])

    else:
        p[0] = gen_p_out('expr',p)


def p_expr_uplus(p):
    '''
    expr : '+' expr %prec UPLUS
    '''
    p[0] = gen_p_out('UPLUS',p)

def p_expr_uminus(p):
    '''
    expr : '-' expr %prec UMINUS
    '''
    p[0] = gen_p_out('UMINUS',p)

def p_expr_uRplus(p):
    '''
    expr : RealPlus expr %prec URPLUS
    '''
    p[0] = gen_p_out('URPLUS',p)

def p_expr_uRminus(p):
    '''
    expr : RealMinus expr %prec URMINUS
    '''
    p[0] = gen_p_out('URMINUS',p)

def p_expr_unot(p):
    '''
    expr : Not expr %prec UNOT
    '''
    p[0] = gen_p_out('UNOT',p)

def p_expr_ubang(p):
    '''
    expr_bang : '!' expr_atom %prec UBANG
    '''
    p[0] = gen_p_out('UBANG',p)


def p_repclause(p):
    '''
    repclause    :   '|' clause repclause
    '''
    p[0] = gen_p_out('repclause',p)

def p_repclause_empty(p):
    '''
    repclause    :   empty
    '''
    pass

def p_clause(p):
    '''
    clause   :   pattern Func expr
    '''
    p[0] = gen_p_out('clause',p)

def p_pattern_atom(p):
    '''
    pattern_atom :   Const_int
                 |   '+' Const_int
                 |   '-' Const_int
                 |   RealPlus Const_float
                 |   RealMinus Const_float
                 |   Const_char
                 |   True
                 |   False
                 |   Identifier
                 |   '(' pattern ')'
    '''
    p[0] = gen_p_out('pattern_atom',p)

def p_pattern(p):
    '''
    pattern  :  pattern_atom reppattern
             |  Constructor reppattern
    '''
    p[0] = gen_p_out('pattern',p)

def p_reppattern(p):
    '''
    reppattern   :  pattern_atom reppattern
                 |  Constructor reppattern
    '''
    p[0] = gen_p_out('reppattern',p)

def p_reppattern_empty(p):
    '''
    reppattern   :  empty
    '''
    pass
