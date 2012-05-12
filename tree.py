#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : tree.py
# Creation Date : 26-04-2012
# Last Modified : Sat 12 May 2012 05:53:40 PM EEST
#_._._._._._._._._._._._._._._._._._._._._.*/

def fixme(stuff):
    ls = []
    for i in stuff.keys():
        ls.append(' {0}="{1}"'.format(i,stuff[i]))
    return "".join(ls)


class node(object):
    def __init__(self,name,stuff,children):
        self._name = name
        self._attrs = stuff
        self._attrsShow = fixme(stuff)
        if children:
            self._children = children
        else:
            self._children = []
        self.type = stuff['type']
    def __repr__(self):
        kids = "".join(map(repr,self._children))
        kids = filter(lambda x: repr(x) != 'None',kids)
        self._attrs['type'] = self.type()
        self._attrsShow = fixme(self._attrs)
        return "<{0} {1}>\n{2}</{0}>\n".format(self._name,self._attrsShow,kids)
        #return "{0}: {1}\n\t{2}".format(self._name,self._attrsShow,self._children)
    def __iter__(self):
        return iter(self._children)
    def symbol(self):
        return self._attrs['symbol']
    def value(self):
        return self._name
    def type(self):
        return self._type



class Node:
    "Base class for all nodes on the abstract syntax tree."
    
    def is_null(self):
        """Returns whether the node represents a null node."""
        
        return 0

    def is_const(self):
        """Returns whether the node is a constant numeric number
        (e.g., "5")."""
        
        return 0
    
    def has_address(self):
        """Returns whether the node has an address (i.e., is a valid
        lvalue)."""
        
        return self.__dict__.has_key("has_addr")

    def set_has_address(self):
        """Tells the node that has an address (is an lvalue).
        Ultimately, the address of the node should be placed in the
        output_addr attribute."""
        
        self.has_addr = 1
        self.output_addr = 0

    def calculate(self):
        """Calculates the constant numeric value of the node and
        its subnodes, if one exists.  For instance, if a node
        corresponds to the expression "5+3", then this method
        would return 8."""
        
        return None
    
    def accept(self, visitor):
        """Accept method for visitor classes (see cvisitor.py)."""
        
        return self._accept(self.__class__, visitor)
        
    def _accept(self, klass, visitor):
        """Accept implementation.  This is actually a recursive
        function that dynamically figures out which visitor method to
        call.  This is done by appending the class' name to 'v', so if
        the node class is called MyNode, then this method tries
        calling visitor.vMyNode().  If that node doesn't exist, then
        it recursively attempts to call the visitor method
        corresponding to the class' superclass (e.g.,
        visitor.vNode())."""
        
        visitor_method = getattr(visitor, "v%s" % klass.__name__, None)
        if visitor_method == None:
            bases = klass.__bases__
            last = None
            for i in bases:
                last = self._accept(i, visitor)
            return last
        else:
            return visitor_method(self)

class NullNode(Node):
    """A null node is like a null terminator for AST's."""

    def __init__(self):
        self.type = 'void'

    def is_null(self):
        return 1

class ArrayExpression(Node):
    """This is an expression with array notation, like "a[5+b]"."""
    
    def __init__(self, expr, index):
        self.expr = expr
        self.index = index

class StringLiteral(Node):
    """A string literal, e.g. the string "Hello World" in
    printf("Hello World")."""
    
    def __init__(self, str):
        self._str = str
        self.type = ArrayOf(BaseType('char'))

    def get_str(self):
        return self._str
    
class Id(Node):
    """An identifier, which can correspond to the name of
    a function, variable, etc..."""

    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno

class Const(Node):
    """A numeric constant (i.e., an integral literal), such as
    the number 5."""
    
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def calculate(self):
        return self.value

    def is_const(self):
        return 1


class Unaryop(Node):
    """Any generic unary operator.  This is an abstract base class."""
    
    def __init__(self, node):
        self.expr = node

class Negative(Unaryop):
    """A negative unary operator, e.g. '-5'."""
    
    def calculate(self):
        val = self.expr.calculate()
        if val != None:
            return -val
        return None

class Positive(Unaryop):
    """A negative unary operator, e.g. '-5'."""
    
    def calculate(self):
        val = self.expr.calculate()
        if val != None:
            return -val
        return None

class Binop(Node):
    """Any binary operator, such as that for arithmetic operations
    (+/-/*), assignment operations (=/+=/-=), and so forth."""

    # List of assignment operators.
    ASSIGN_OPS = [':=']
    
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def calculate(self):
        left = self.left.calculate()
        right = self.right.calculate()
        if left != None and right != None:
            if self.op == ':=':
                op = '='
                return int(eval("%d %s %d" % (left, op, right)))
            else:
                return None
        else:
            return None

class IfStatement(Node):
    """An if/then/else statement."""
    
    def __init__(self, expr, then_stmt, else_stmt):
        self.expr = expr
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

class ReturnStatement(Node):
    """A return statement, used to exit a function and optionally
    return a value."""
    
    def __init__(self, expr):
        self.expr = expr

class ForLoop(Node):
    """A for loop."""
    
    def __init__(self, begin_stmt, expr, end_stmt, stmt):
        self.expr = expr
        self.stmt = stmt
        self.begin_stmt = begin_stmt
        self.end_stmt = end_stmt

class WhileLoop(Node):
    """A while loop."""
    
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt

class NodeList(Node):
    """A list of nodes.  This is an abstract base class."""
    
    def __init__(self, node=None):
        self.nodes = []
        if node != None:
            self.nodes.append(node)

    def add(self, node):
        if node != None:
            self.nodes.append(node)

class TranslationUnit(NodeList):
    """A list of nodes representing the program itself."""

    pass

class ArgumentList(NodeList):
    """A list of arguments for a function expression.  e.g., the list
    '5,2,3' in 'a = my_func(5,2,3)'."""
    
    pass

class ParamList(NodeList):
    """A list of parameters for a function prototype, e.g. the list
    'int a, char b, char c' in 'int my_func(int a, char b, char c)'."""

    def __init__(self, node=None):
        NodeList.__init__(self, node)
        self.has_ellipsis = 0

class StatementList(NodeList):
    """Any list of statements.  For instance, this can be the list of
    statements in a function body."""

    pass

class FunctionExpression(Node):
    """An execution o f a function, e.g. 'my_func(a,b,c)'."""
    
    def __init__(self, function, arglist):
        self.function =  function
        self.arglist = arglist

class FunctionDefn(Node):
    """A node representing a function definition (its declaration
    and body)."""
    
    def __init__(self, declaration, body):
        self.type = declaration.type
        self.name = declaration.name
        self.body = body

class Declaration(Node):
    """A node represe nting a declaration of a function or
    variable."""
    
    def __init__(self, name, type=None):
        if type == None:
            type = NullNode()
        self.type = type
        self.name = name
        self.is_used = 0

    def set_base_type(self, type):
        if self.type.is_null():
            self.type = type
        else:
            self.type.set_base_type(type)

    def add_type(self, type):
        type.set_base_type(self.type)
        self.type = type

#  ---------------------------------------------------------------
#  ABSTRACT SYNTAX TREE - TYPE SYSTEM
#  ---------------------------------------------------------------

class Type(Node):
    """A node representing the type of another node.  For instance,
    the Binop node representing '5 + a', where a is an int, will have
    a Type node associated with it that represents the fact that
    the result of the Binop is an int.

    Types can also be nested, so that for instance you can have
    a type like 'pointer(pointer(int))' which represents a
    double-pointer to an int.

    This is an abstract base class."""
    
    def __init__(self, child=None):
        if child == None:
            child = NullNode()
        self.child = child

    def set_base_type(self, type):
        """Set the base (innermost) type of a type.  For instance,
        calling this with a pointer(int) type on a pointer() type
        will give you a pointer(pointer(int))."""
        
        if self.child.is_null():
            self.child = type
        else:
            self.child.set_base_type(type)

    def get_string(self):
        """Return a string corresponding to the type, e.g.
        'pointer(pointer(int))'."""
        
        raise NotImplementedError()

    def get_outer_string(self):
        """Return only the outermost type of a type.  e.g.,
        calling this on a pointer(pointer(int)) type will
        return 'pointer'."""
        
        raise NotImplementedError()

    def is_function(self):
        """Returns whether or not this type represents a
        function."""
        
        return 0

class BaseType(Type):
    """A base type representing ints, chars, etc..."""
    
    def __init__(self, type_str, child=None):
        Type.__init__(self, child)
        self.type_str = type_str

    def get_string(self):
        return self.type_str

    def get_outer_string(self):
        return self.type_str

class FunctionType(Type):
    """A type representing a function (for function prototypes and
    function calls)."""
    
    def __init__(self, params=None, child=None):
        Type.__init__(self, child)
        if (params == None):
            params = NullNode()
        self.params = params

    def get_string(self):
        param_str = ""
        for param in self.params.nodes:
            param_str += "," + param.type.get_string()
        return "function(%s)->%s" % (param_str[1:], self.child.get_string())

    def get_outer_string(self):
        return 'function'

    def is_function(self):
        return 1

    def get_return_type(self):
        """Returns the return type of the function.  Internally,
        this is stored as the nested type within the function."""
        
        return self.child

    def get_params(self):
        """Returns the list of parameters for the function."""
        
        return self.params

#  ---------------------------------------------------------------
#  PARSER GRAMMAR / AST CONSTRUCTION
#
#  The only thing the yacc grammar rules do is create an
#  abstract syntax tree.  Actual symbol table generation,
#  type checking, flow control checking, etc. are done by
#  the visitor classes (see cvisitors.py).
#  ---------------------------------------------------------------

# Precedence for ambiguous grammar elements.
precedence = (
    ('right', 'ELSE'),
)

class ParseError(Exception):
    "Exception raised whenever a parsing error occurs."

    pass

def p_translation_unit_01(t):
    '''translation_unit : external_declaration'''
    t[0] = TranslationUnit(t[1])

def p_translation_unit_02(t):
    '''translation_unit : translation_unit external_declaration'''
    t[1].add(t[2])
    t[0] = t[1]

def p_external_declaration(t):
    '''external_declaration : function_definition
                            | declaration'''
    t[0] = t[1]

def p_function_definition_01(t):
    '''function_definition : type_specifier declarator compound_statement'''
    t[2].set_base_type(t[1])
    t[0] = FunctionDefn(t[2], t[3])

def p_function_definition_02(t):
    '''function_definition : STATIC type_specifier declarator compound_statement'''
    t[3].static = 1
    t[3].set_base_type(t[2])
    t[0] = FunctionDefn(t[3], t[4])
    
def p_declaration_01(t):
    '''declaration : type_specifier declarator SEMICOLON'''
    if isinstance(t[2].type, FunctionType):
        t[2].extern = 1
    t[2].set_base_type(t[1])
    t[0] = t[2]

def p_declaration_02(t):
    '''declaration : EXTERN type_specifier declarator SEMICOLON'''
    t[3].extern = 1
    t[3].set_base_type(t[2])
    t[0] = t[3]

def p_declaration_list_opt_01(t):
    '''declaration_list_opt : empty'''
    t[0] = NullNode()

def p_declaration_list_opt_02(t):
    '''declaration_list_opt : declaration_list'''
    t[0] = t[1]

def p_declaration_list_02(t):
    '''declaration_list : declaration'''
    t[0] = DeclarationList(t[1])

def p_declaration_list_03(t):
    '''declaration_list : declaration_list declaration'''
    t[1].add(t[2])
    t[0] = t[1]
    
def p_type_specifier(t):
    '''type_specifier : INT
                      | CHAR'''
    t[0] = BaseType(t[1])

def p_declarator_01(t):
    '''declarator : direct_declarator'''
    t[0] = t[1]

def p_declarator_02(t):
    '''declarator : ASTERISK declarator'''
    t[2].set_base_type(PointerType())
    t[0] = t[2]

def p_direct_declarator_01(t):
    '''direct_declarator : ID'''
    t[0] = Declaration(t[1])

def p_direct_declarator_02(t):
    '''direct_declarator : direct_declarator LPAREN parameter_type_list RPAREN'''
    t[1].add_type(FunctionType(t[3]))
    t[0] = t[1]

def p_direct_declarator_03(t):
    '''direct_declarator : direct_declarator LPAREN RPAREN'''
    t[1].add_type(FunctionType(ParamList()))
    t[0] = t[1]
    
def p_parameter_type_list_01(t):
    '''parameter_type_list : parameter_list'''
    t[0] = t[1]

def p_parameter_type_list_02(t):
    '''parameter_type_list : parameter_list COMMA ELLIPSIS'''
    t[1].has_ellipsis = 1
    t[0] = t[1]

def p_parameter_list_01(t):
    '''parameter_list : parameter_declaration'''
    t[0] = ParamList(t[1])

def p_parameter_list_02(t):
    '''parameter_list : parameter_list COMMA parameter_declaration'''
    t[1].add(t[3])
    t[0] = t[1]

def p_parameter_declaration(t):
    '''parameter_declaration : type_specifier declarator'''
    # NOTE: this is the same code as p_declaration_01!
    p_declaration_01(t)

def p_compound_statement_01(t):
    '''compound_statement : LBRACE declaration_list_opt statement_list RBRACE'''
    t[0] = CompoundStatement(t[2], t[3])

def p_compound_statement_02(t):
    '''compound_statement : LBRACE declaration_list_opt RBRACE'''
    t[0] = CompoundStatement(t[2], NullNode())

def p_expression_statement(t):
    '''expression_statement : expression SEMICOLON'''
    t[0] = t[1]

def p_expression_01(t):
    '''expression : equality_expression'''
    t[0] = t[1]

def p_expression_02(t):    
    '''expression : equality_expression ASSIGN expression
                  | equality_expression EQ_PLUS expression
                  | equality_expression EQ_MINUS expression'''
    t[0] = Binop(t[1], t[3], t[2])

def p_equality_expression_01(t):
    '''equality_expression : relational_expression'''
    t[0] = t[1]

def p_equality_expression_02(t):    
    '''equality_expression : equality_expression EQ relational_expression
                           | equality_expression NOT_EQ relational_expression'''
    t[0] = _get_calculated(Binop(t[1], t[3], t[2]))

def p_relational_expression_01(t):
    '''relational_expression : additive_expression'''
    t[0] = t[1]

def p_relational_expression_02(t):
    '''relational_expression : relational_expression LESS additive_expression
                             | relational_expression GREATER additive_expression
                             | relational_expression LESS_EQ additive_expression
                             | relational_expression GREATER_EQ additive_expression'''
    t[0] = _get_calculated(Binop(t[1], t[3], t[2]))

def p_postfix_expression_01(t):
    '''postfix_expression : primary_expression'''
    t[0] = t[1]

def p_postfix_expression_02(t):
    '''postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'''
    t[0] = FunctionExpression(t[1], t[3])
    pass

def p_postfix_expression_03(t):
    '''postfix_expression : postfix_expression LPAREN RPAREN'''
    t[0] = FunctionExpression(t[1], ArgumentList())

def p_postfix_expression_04(t):
    '''postfix_expression : postfix_expression LBRACKET expression RBRACKET'''
    t[0] = ArrayExpression(t[1], t[3])

def p_argument_expression_list_01(t):
    '''argument_expression_list : expression'''
    t[0] = ArgumentList(t[1])

def p_argument_expression_list_02(t):
    '''argument_expression_list : argument_expression_list COMMA expression'''
    t[1].add(t[3])
    t[0] = t[1]

def p_unary_expression_01(t):
    '''unary_expression : postfix_expression'''
    t[0] = t[1]

def p_unary_expression_02(t):
    '''unary_expression : MINUS unary_expression'''
    t[0] = _get_calculated(Negative(t[2]))

def p_unary_expression_03(t):
    '''unary_expression : PLUS unary_expression'''
    t[0] = t[2]

def p_unary_expression_03(t):
    '''unary_expression : EXCLAMATION unary_expression'''
    # horrible hack for the '!' operator... Just insert an
    # (expr == 0) into the AST.
    t[0] = _get_calculated(Binop(t[2], Const(0, BaseType('int')), '=='))

def p_unary_expression_04(t):
    '''unary_expression : ASTERISK unary_expression'''
    t[0] = Pointer(t[2])

def p_unary_expression_05(t):
    '''unary_expression : AMPERSAND unary_expression'''
    t[0] = AddrOf(t[2])

def p_mult_expression_01(t):
    '''mult_expression : unary_expression'''
    t[0] = t[1]

def p_mult_expression_02(t):
    '''mult_expression : mult_expression ASTERISK unary_expression
                       | mult_expression DIV unary_expression    
                       | mult_expression MODULO unary_expression'''
    t[0] = _get_calculated(Binop(t[1], t[3], t[2]))

def p_additive_expression_01(t):
    '''additive_expression : mult_expression'''
    t[0] = t[1]

def p_additive_expression_02(t):
    '''additive_expression : additive_expression PLUS mult_expression
                           | additive_expression MINUS mult_expression'''
    t[0] = _get_calculated(Binop(t[1], t[3], t[2]))

def p_primary_expression_01(t):
    '''primary_expression : ID'''
    t[0] = Id(t[1], t.lineno(1))

def p_primary_expression_02(t):
    '''primary_expression : INUMBER'''
    t[0] = Const(int(t[1]), BaseType('int'))

def p_primary_expression_03(t):
    '''primary_expression : FNUMBER'''
    t[0] = Const(float(t[1]), BaseType('double'))

def p_primary_expression_04(t):
    '''primary_expression : CHARACTER'''
    t[0] = Const(ord(eval(t[1])), BaseType('char'))

def p_primary_expression_05(t):
    '''primary_expression : string_literal'''
    t[0] = t[1]

def p_primary_expression_06(t):
    '''primary_expression : LPAREN expression RPAREN'''
    t[0] = t[2]

def p_string_literal_01(t):
    '''string_literal : STRING'''
    t[0] = StringLiteral(eval(t[1]))

def p_string_literal_02(t):
    '''string_literal : string_literal STRING'''
    t[1].append_str(eval(t[2]))
    t[0] = t[1]

def p_statement(t):
    '''statement : compound_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement'''
    t[0] = t[1]

def p_jump_statement_01(t):
    '''jump_statement : RETURN SEMICOLON'''
    t[0] = ReturnStatement(NullNode())
    
def p_jump_statement_02(t):
    '''jump_statement : RETURN expression SEMICOLON'''
    t[0] = ReturnStatement(t[2])

def p_jump_statement_03(t):
    '''jump_statement : BREAK SEMICOLON'''
    t[0] = BreakStatement()

def p_jump_statement_04(t):
    '''jump_statement : CONTINUE SEMICOLON'''
    t[0] = ContinueStatement()

def p_iteration_statement_01(t):
    '''iteration_statement : WHILE LPAREN expression RPAREN statement'''
    t[0] = WhileLoop(t[3], t[5])

def p_iteration_statement_02(t):
    '''iteration_statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement'''
    t[0] = ForLoop(t[3], t[4], t[5], t[7])

def p_selection_statement_01(t):
    '''selection_statement : IF LPAREN expression RPAREN statement'''
    t[0] = IfStatement(t[3], t[5], NullNode())

def p_selection_statement_02(t):
    '''selection_statement : IF LPAREN expression RPAREN statement ELSE statement'''
    t[0] = IfStatement(t[3], t[5], t[7])

def p_statement_list_02(t):
    '''statement_list : statement'''
    t[0] = StatementList(t[1])

def p_statement_list_03(t):
    '''statement_list : statement_list statement'''
    t[1].add(t[2])
    t[0] = t[1]

def p_empty(t):
    'empty :'
    pass

def p_error(t):
    print "You've got a syntax error somewhere in your code."
    print "It could be around line %d." % t.lineno
    print "Good luck finding it."
    raise ParseError()

yacc.yacc(debug=1)

#  ---------------------------------------------------------------
#  End of cparse.py
#  ---------------------------------------------------------------







