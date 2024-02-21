from lex import lex
from yacc import yacc

# All tokens must be named in advance.
tokens = ( 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
           'NAME', 'NUMBER','AND','OR','SORT','LBRA','RBRA','EQUAL',
            'COM','QUOTE','PERIOD','SCOLN' )

t_ignore = ' \t'

t_PLUS= r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER= r'\d+'
t_AND=r'\&'
t_OR=r'\|'
t_SORT= r'\>'
t_LBRA=r'\['
t_RBRA=r'\]'
t_COM=r'\,'
t_QUOTE=r'\"|\''
t_PERIOD=r'\.'
t_SCOLN=r'\;'

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

lexer = lex()


data = " 3+ 6"

# Give the lexer some input
lexer.input(data)

# Tokenize the input
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)

def p_expression(p):
    '''
    expression : term PLUS term
               | term MINUS term
    '''
    # p is a sequence that represents rule contents.
    #
    # expression : term PLUS term
    #   p[0]     : p[1] p[2] p[3]
    # 
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : factor TIMES factor
         | factor DIVIDE factor
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor_number(p):
    '''
    factor : NUMBER
    '''
    p[0] = ('number', p[1])

def p_factor_name(p):
    '''
    factor : NAME
    '''
    p[0] = ('name', p[1])

def p_factor_unary(p):
    '''
    factor : PLUS factor
           | MINUS factor
    '''
    p[0] = ('unary', p[1], p[2])

def p_factor_grouped(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = ('grouped', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('2 * 3 + 4 * (5 - x)')
print(ast)
