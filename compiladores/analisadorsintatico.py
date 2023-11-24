import ply.yacc as yacc
import ply.lex as lex
import Complemento

t_PLUS = r'\+'
t_MINUS = r'\-'
t_EQUALS = r'='
t_ASTERISC = r'\*'
t_DOUBLEEQUALS = r'=='
t_SLASH = r'/'
t_PERCENT = r'%'
t_AND = r'&&'
t_OR = r'\|\|'
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_THAN_EQUAL = r'<='
t_GREATER_THAN_EQUAL = r'>='
t_NOT_EQUAL = r'!='
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'

def t_COMMENT(t):
    r'\/\/[^\n]*'
    return t

def t_COMMENT_MULTI(t):
    r'\/\*[\s\S]*?\*\/'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in Complemento.palavras_reservadas:
        t.type = Complemento.palavras_reservadas.get(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

def t_DECIMAL_NUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t


def t_BOOL(t):
    r'false|true'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore  = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
def lexico(arquivo):
    tokens = Complemento.TIPOS + list(Complemento.palavras_reservadas.values()) + list(Complemento.OPERADORES_E_SIMBOLOS_E.values())
    lexer = lex.lex()

    with open(arquivo, 'r') as file:
        data = file.read()  

    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break  
        print(tok)

lexico('compiladores\input.txt') 


tokens = Complemento.TIPOS + list(Complemento.palavras_reservadas.values()) + list(Complemento.OPERADORES_E_SIMBOLOS_E.values())

def p_programa(p):
    '''programa : declaracao'''

def p_declaracao(p):
    '''
    declaracao : declaracao_variavel
    declaracao : declaracao_funcao
    declaracao : declaracao_estrutura
    declaracao : comentario
    declaracao_variavel : tipo ID SEMICOLON | tipo ID EQUALS expressao SEMICOLON

    '''

def p_tipo(p):
    '''
    tipo : INT_PALAVRA_RESERVADA | FLOAT_PALAVRA_RESERVADA | DOUBLE_PALAVRA_RESERVADA | CHAR_PALAVRA_RESERVADA | BOOLEAN_PALAVRA_RESERVADA
    
    '''



parser = yacc.yacc()
s = Complemento.codigo()
parser.parse(s)
print("sintatico ok")
