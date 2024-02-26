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
