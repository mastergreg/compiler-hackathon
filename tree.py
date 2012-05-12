#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : tree.py
# Creation Date : 26-04-2012
# Last Modified : Sat 12 May 2012 08:45:16 PM EEST
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

class Not(Unaryop):
    def calculate(self):
        val = self.expr.calculate()
        if val != None:
            return not val
        return None

class Negative(Unaryop):
    def calculate(self):
        val = self.expr.calculate()
        if val != None:
            return -val
        return None

class Positive(Unaryop):
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
    
    def __init__(self, expr, then_stmt):
        self.expr = expr
        self.then_stmt = then_stmt

class IfElseStatement(Node):
    """An if/then/else statement."""
    
    def __init__(self, expr, then_stmt, else_stmt):
        self.expr = expr
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

class ReturnStatement(Node):
    def __init__(self, expr=None):
        self.expr = expr

class Statement(Node):
    def __init__(self, expr):
        self.expr = expr

class SizeStatement(Node):
    def __init__(self, expr):
        self.expr = expr

class NewStatement(Node):
    def __init__(self, type, expr):
        self.type = type
        self.size = expr

class DeleteStatement(Node):
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

class Visitor:
    """The base visitor class.  This is an abstract base class."""

    def __init__(self):
        self.warnings = 0
        self.errors = 0

    def _visitList(self, list):
        """Visit a list of nodes.  'list' should be an actual list,
        not a cparse.NodeList object."""
        
        last = None
        for i in list:
            last = i.accept(self)
        return last
    
    def visit(self, node):
        """Visits the given node by telling the node to call the
        visitor's class-specific visitor method for that node's
        class (i.e., double dispatching)."""
        
        return node.accept(self)

    def warning(self, str):
        """Output a non-fatal compilation warning."""
        
        print "warning: %s" % str
        self.warnings += 1

    def error(self, str):
        """Output a fatal compilation error."""
        
        print "error: %s" % str
        self.errors += 1

    def has_errors(self):
        """Returns whether the visitor has encountered any
        errors."""
        
        return self.errors > 0


class ASTPrinterVisitor(Visitor):
    """Simple visitor that outputs a textual representation of
    the abstract syntax tree, for debugging purposes, to an
    output file."""
    
    def __init__(self, ast_file, indent_amt=2):
        self.ast_file = ast_file
        Visitor.__init__(self)
        self._indent = 0
        self._indent_amt = indent_amt

    def indent(self):
        self._indent += self._indent_amt

    def unindent(self):
        self._indent -= self._indent_amt

    def p(self, str):
        self.ast_file.write(
            (' ' * (self._indent_amt * self._indent) ) + str + "\n" )

    def pNodeInfo(self, node):
        # Print out the name of the node's class.
        self.p('+ ' + node.__class__.__name__)

        # If the node has a type associated with it,
        # print the string of the type.
        if node.__dict__.has_key("type"):
            self.p("  Type-string: %s" % node.type.get_string())

        # Find all attributes of the node that are ints or
        # strings and aren't 'private' (i.e., don't begin with
        # '_'), and print their values.
        for key in node.__dict__.keys():
            if key[0] == '_':
                continue
            val = node.__dict__[key]
            if (isinstance(val, str) or
                isinstance(val, int)):
                self.p("  %s: %s" % (key, str(val)))

    def pSubnodeInfo(self, subnode, label):
        if not subnode.is_null():
            self.p("  %s:" % label)
            self.indent()
            subnode.accept(self)
            self.unindent()

    def vNullNode(self, node):
        self.pNodeInfo(node)

    def vArrayExpression(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.expr, "Expression")
        self.pSubnodeInfo(node.index, "Index")

    def vStringLiteral(self, node):
        self.pNodeInfo(node)
        self.p('  Value: "%s"' % node.get_sanitized_str())

    def vId(self, node):
        self.pNodeInfo(node)

    def vUnaryop(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.expr, "Expression")

    def vFunctionExpression(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.function, "Function")
        self.pSubnodeInfo(node.arglist, "Arguments")

    def vConst(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.type, "Type")

    def vBinop(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.left, "Left operand")
        self.pSubnodeInfo(node.right, "Right operand")

    def vNodeList(self, node):
        self.pNodeInfo(node)
        self.indent()
        self._visitList(node.nodes)
        self.unindent()

    def vCompoundStatement(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.declaration_list, "Declaration list")
        self.pSubnodeInfo(node.statement_list, "Statement list")        

    def vBaseType(self, node):
        self.pNodeInfo(node)

    def vFunctionType(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.params, "Parameters:")
        self.pSubnodeInfo(node.child, "Child:")

    def vPointerType(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.child, "Child:")

    def vDeclaration(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.type, "Type")

    def vReturnStatement(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.expr, "Expression")

    def vFunctionDefn(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.type, "Type")
        self.pSubnodeInfo(node.body, "Body")

    def vIfStatement(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.expr, "Expression")
        self.pSubnodeInfo(node.then_stmt, "Then statement")
        self.pSubnodeInfo(node.else_stmt, "Else statement")

    def vWhileLoop(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.expr, "Expression")
        self.pSubnodeInfo(node.stmt, "Statement")

    def vForLoop(self, node):
        self.pNodeInfo(node)
        self.pSubnodeInfo(node.begin_stmt, "Begin statement")
        self.pSubnodeInfo(node.expr, "Test expression")
        self.pSubnodeInfo(node.end_stmt, "End statement")
        self.pSubnodeInfo(node.stmt, "Statement")

