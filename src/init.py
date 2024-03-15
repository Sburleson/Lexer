from lex import lex
from yacc import yacc

# All tokens must be named in advance.
tokens = ( 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
           'NAME', 'NUMBER','AND','OR','GR8R','LBRA','RBRA','EQUAL',
            'COM','QUOTE','PERIOD','SCOLN','COMPEQU','LES', 'MOD', 'SORT')

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
t_GR8R= r'\>'
t_LBRA=r'\['
t_RBRA=r'\]'
t_COM=r'\,'
t_QUOTE=r'\"|\''
t_PERIOD=r'\.'
t_SCOLN=r'\;'
t_COMPEQU=r'\=='
t_LES=r'\<'
t_MOD=r'\%'
t_SORT=r'\>>'

## keywords

t_FOR=r'\FOR'
t_WHILE=r'\WHILE'
T_IF=r'\IF'
T_ELSE=r'\ELSE'
T_RETURN=r'RETURN'
T_SLEEP=r'SLEEP'
T_VAR=r'VAR'
T_TRY=r'TRY'
T_CATCH=r'CATCH'
T_COMMENT=r'//'


def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

lexer = lex()


data = "3+ 6"

# Give the lexer some input
lexer.input(data)

# Tokenize the input
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)



### define the grammar
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()
    
# --- Parser

# Write functions for each grammar rule which is
# specified in the docstring.
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

def p_statement_for(p):
    '''
    statement : FOR LPAREN expression SCOLN expression SCOLN expression RPAREN expression
    '''
    p[0] = ('for_loop', p[3], p[5], p[7], p[9])

def p_statement_while(p):
    '''
    statement : WHILE LPAREN expression RPAREN expression
    '''
    p[0] = ('while_loop', p[3], p[5])

def p_statement_if(p):
    '''
    statement : IF LPAREN expression RPAREN expression
    '''
    p[0] = ('if_statement', p[3], p[5])

def p_statement_if_else(p):
    '''
    statement : IF LPAREN expression RPAREN expression ELSE expression
    '''
    p[0] = ('if_else_statement', p[3], p[5], p[7])


def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('2 * 3 + 4 * (5 - x)')
print(ast)
