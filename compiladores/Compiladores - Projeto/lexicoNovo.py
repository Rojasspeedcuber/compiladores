import ply.lex as lex
import Complemento

t_PLUS = r'\+'
t_MINUS = r'\-'

def t_COMENTARIO(t):
    r'\/\/[^\n]*'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in Complemento.palavras_reservadas:
        t.type = Complemento.palavras_reservadas.get(t.value)
    return t
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_BOOLEAN(t):
    r'false|true'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
def lexico():
    tokens = Complemento.TIPOS + list(Complemento.palavras_reservadas.values()) + list(Complemento.OPERADOR.values())
    lexer = lex.lex()
    data = 'int + -'
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)
        
lexico()