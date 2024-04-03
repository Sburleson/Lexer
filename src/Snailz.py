from ply import lex
from ply import yacc
import os

class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children else []
        self.value = value

class Parser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[
                1] + "_" + self.__class__.__name__
        except:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"
        # print self.debugfile

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile)

    def run(self):
        while True:
            try:
                s = input('snailz > ')
            except EOFError:
                break
            if not s:
                continue
            self.parse_result = yacc.parse(s)
            if self.parse_result:
                self.print_ast(self.parse_result)


class Snailz(Parser):
    
    tokens =  ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
           'NAME', 'NUMBER', 'AND', 'OR', 'GR8R', 'LBRA', 'RBRA', 'COM', 'QUOTE',
           'PERIOD', 'SCOLN', 'COMPEQU', 'EQUALS', 'LES', 'MOD', 'SORT',
           'NOT', 'VAR', 'EXP')
   
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_AND = r'\&'
    t_OR = r'\|'
    t_GR8R = r'\>'
    t_LBRA = r'\['
    t_RBRA = r'\]'
    t_COM = r'\,'
    t_QUOTE = r'\"|\''
    t_PERIOD = r'\.'
    t_SCOLN = r'\;'
    t_COMPEQU = r'\=='
    t_EQUALS = r'\='
    t_LES = r'\<'
    t_MOD = r'\%'
    t_SORT = r'\>>'
    t_NOT = r'\!'
    t_VAR = r'[\w]+'
    t_EXP = r'\^'

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        # print "parsed number %s" % repr(t.value)
        return t

    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Parsing rules

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'EXP'),
        ('right', 'UMINUS'),
    )

    def p_statement_assign(self, p):
        'statement : NAME EQUALS expression'
        p[0] = ASTNode('assignment', [ASTNode('variable', value=p[1]), p[3]])

    def p_statement_expr(self, p):
        'statement : expression'
        p[0] = p[1]

    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EXP expression
        """
        p[0] = ASTNode(p[2], [p[1], p[3]])

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = ASTNode('uminus', [p[2]])

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = ASTNode('number', value=p[1])

    def p_expression_name(self, p):
        'expression : NAME'
        p[0] = ASTNode('variable', value=p[1])

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    # Method to print the AST
    def print_ast(self, node, indent=0):
        print(' ' * indent + node.type)
        if node.value is not None:
            print(' ' * (indent + 2) + str(node.value))
        for child in node.children:
            self.print_ast(child, indent + 2)

if __name__ == '__main__':
    snailz = Snailz()
    snailz.run()

    # After parsing, print the AST
    ast_root = snailz.parse_result
    snailz.print_ast(ast_root)