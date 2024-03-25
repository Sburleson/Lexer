from lex import lex
from yacc import yacc

# All tokens must be named in advance.
tokens = ( 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
           'NAME', 'NUMBER','AND','OR','GR8R','LBRA','RBRA','EQUAL',
            'COM','QUOTE','PERIOD','SCOLN','COMPEQU','LES', 'MOD', 'SORT', 
            'FOR', 'WHILE','IF','ELSE','RETURN','SLEEP','VAR','TRY','CATCH', 
            'COMMENT','NOT','SHELL', 'SLOW', 'SLIME', 'SPIRAL', 'SNAIL', 'ESCARGO' )

t_ignore = ' \t'

t_PLUS= r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
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
t_NOT=r'\!'
t_NUMBER = r'\d+'

## keywords
t_SHELL = r'SHELL'
t_SLOW = r'SLOW'
t_SLIME = r'SLIME'
t_SPIRAL = r'SPIRAL'
t_SNAIL = r'SNAIL'
t_ESCARGO = r'ESCARGO'
t_FOR=r'FOR'
t_WHILE=r'WHILE'
T_IF=r'IF'
T_ELSE=r'ELSE'
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

def t_TUPLE(t):
    r'\(\d{1,2}-\d{1,2}\)'
    t.value = tuple(map(int, re.findall(r'\d{1,2}', t.value)))
    return t

def t_4BYTE(t):
    r'4 byte \d{1,9}'
    t.value = int(t.value.split()[2])
    return t

def t_8BYTE(t):
    r'8 byte \d{1,9}'
    t.value = int(t.value.split()[2])
    return t

def t_TRUE_FALSE(t):
    r'True|False'
    t.value = True if t.value == 'True' else False
    return t



# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


def p_bool_expr(p):
  '''
  bool_expr : term OR term
            | term AND term  # You might already have AND defined
            | NOT term  # Optional: Add NOT operator
            | bool_expr EQUALS bool_expr  # Add comparison operators if needed
            | ...  # Add other boolean operators (e.g., XOR)
  '''
# Build the lexer object
lexer = lex()
    
# --- Parser

# Write functions for each grammar rule which is
# specified in the docstring.
def p_data_type(p):
    '''
    data_type : SHELL LPAREN NUMBER MINUS NUMBER RPAREN
              | SLOW NUMBER
              | SLIME NUMBER
              | SPIRAL TRUE_FALSE
              | SNAIL NAME
              | ESCARGO NAME
    '''
    # Depending on the data type, you can handle the parsed values accordingly
    if p[1] == 'Shell':
        p[0] = ('shell', (p[3], p[5]))  # Assuming 'shell' as the data type
    elif p[1] == 'Slow':
        p[0] = ('slow', p[2])  # Assuming 'slow' as the data type
    elif p[1] == 'Slime':
        p[0] = ('slime', p[2])  # Assuming 'slime' as the data type
    elif p[1] == 'Spiral':
        p[0] = ('spiral', p[2])  # Assuming 'spiral' as the data type
    elif p[1] == 'Snail':
        p[0] = ('snail', p[2])  # Assuming 'snail' as the data type
    elif p[1] == 'Escargo':
        p[0] = ('escargo', p[2])  # Assuming 'escargo' as the data type
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
def p_expression_mod(p):
    '''
    expression : term MOD term
    '''
    p[0] = ('modulo', p[2], p[1], p[3])
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

def p_statement_assignment(p):
    '''
    statement : NAME EQUAL expression
    '''
    p[0] = ('assignment', p[1], p[3])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

def t_COMMENT(t):
    r'\//.*'
    pass

def p_expression_brackets(p):
    '''
    expression : LBRA expression RBRA
    '''
    p[0] = ('brackets', p[2])

def p_expression_comparison(p):
    '''
    expression : term GR8R term
             | term LES term
             | term COMPEQU term
    '''
    p[0] = ('comparison', p[2], p[1], p[3])

def p_list(p):
    '''
    list : LBRA term COM list  # Base case: list starts with term and ends with comma-separated terms
       | LBRA term RBRA     # Single term list
    '''
    if len(p) == 4:  # List with multiple terms
        p[0] = ('list', p[2], p[4])  # Build AST with first term and remaining list
    else:
        p[0] = ('list', p[2])  # Single term list

def p_term(p):
    '''
    term : NUMBER
       | NAME
       | ...  # Other types of terms
    '''
def p_string(p):
    '''
    string : QUOTE chars QUOTE
    '''
    p[0] = ('string', p[2])  # Build AST with the characters inside the quotes

def p_statement(p):
    '''
    statement : expression
            | SEMICOLON  # Empty statement
    '''
def p_expression_custom(p):
    '''
    expression : list SORT  # Assuming DOUBLE_RIGHT_SHIFT defined for >>
    '''
  # Implement custom logic for the >> operator in the context of Bogosort
    p[0] = ('custom_operator', p[2], p[1], p[3])  # Example AST representation
def p_statement_return(p):
    '''
    statement : RETURN
    '''
def p_statement_return(p):
    '''
    statement : RETURN expression
    '''
    p[0] = ('return', p[2])

def p_statement(p):
    '''
    statement : SLEEP
    '''
    # Handle sleep functionality (potentially using external libraries)
def p_var_declaration(p):
    '''
    var_declaration : VAR NAME EQUAL expression
                    | VAR NAME
    '''
    if len(p) == 5:
        p[0] = ('var_declaration', p[2], p[4])  # If the variable is assigned a value
    else:
        p[0] = ('var_declaration', p[2], None)  # If the variable is just declared
def p_try_catch(p):
    '''
    try_catch : TRY statement_list catch_blocks
    '''
    p[0] = ('try_catch', p[2], p[3])

def p_catch_blocks(p):
    '''
    catch_blocks : catch_block
                 | catch_block catch_blocks
    '''
    if len(p) == 2:
        p[0] = [p[1]]  # Single catch block
    else:
        p[0] = [p[1]] + p[2]  # Multiple catch blocks

def p_catch_block(p):
    '''
    catch_block : CATCH LPAREN NAME RPAREN statement_list
    '''
    p[0] = ('catch_block', p[3], p[5])


# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('2 * 3 + 4 * (5 - x)')
print(ast)
