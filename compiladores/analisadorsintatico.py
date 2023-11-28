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
t_LKEY = r'\{'
t_RKEY = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_TWOPOINTS = r':'
t_ARROW = r'->'
t_DOT = r'.'

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
    '''
    programa : declaracao
    '''

def p_declaracao(p):
    '''
    declaracao : declaracao_variavel
    declaracao : declaracao_funcao
    declaracao : declaracao_estrutura
    declaracao : comentario
    declaracao_variavel : tipo ID SEMICOLON | tipo ID EQUALS expressao SEMICOLON
    declaracao_funcao : tipo ID LPAREN parametros RPAREN bloco
    declaracao_estrutura : struct ID LKEY declaracao_variavel* RKEY SEMICOLON
    '''
def p_bloco(p):
    '''
    bloco : LKEY declaracao* RKEY
    '''
def p_parametros(p):
    '''
    parametros : parametro
    parametros : parametro COMMA parametros
    parametro : tipo ID
    parametro : tipo ID LBRACKET RBRACKET
    '''
def p_estruturas_controle(p):
    '''
    estrutura_controle : IF_PALAVRA_RESERVADA LPAREN expressao RPAREN bloco
    estrutura_controle : IF_PALAVRA_RESERVADA LPAREN expressao RPAREN bloco ELSE_PALAVRA_RESERVADA bloco
    estrutura_controle : WHILE_PALAVRA_RESERVADA LPAREN expressao RPAREN bloco
    estrutura_controle : FOR_PALAVRA_RESERVADA LPAREN expressao SEMICOLON expressao SEMICOLON expressao RPAREN bloco
    estrutura_controle : SWITCH_PALAVRA_RESERVADA LPAREN expressao RPAREN case_lista
    case_lista : case_decl*
    case_decl : CASE_PALAVRA_RESERVADA expressao TWOPOINTS bloco
    case_decl : DEFAULT_PALAVRA_RESERVADA TWOPOINTS bloco
    estrutura_controle : BREAK_PALAVRA_RESERVADA SEMICOLON
    estrutura_controle : CONTINUE_PALAVRA_RESERVADA SEMICOLON
    estrutura_controle : RETURN_PALAVRA_RESERVADA expressao SEMICOLON
    '''
def p_expressoes(p):
    '''
    expressao : atribuicao
    atribuicao : ID EQUALS expressao
    atribuicao : ID PLUS EQUALS expressao
    atribuicao : ID MINUS EQUALS expressao
    atribuicao : ID ASTERISC EQUALS expressao
    atribuicao : ID SLASH EQUALS expressao
    atribuicao : ID PERCENT EQUALS expressao
    atribuicao : ID AND EQUALS expressao
    atribuicao : ID OR EQUALS expressao
    atribuicao : ID EQUALS ID
    atribuicao : ID PLUS EQUALS ID
    atribuicao : ID MINUS EQUALS ID
    atribuicao : ID ASTERISC EQUALS ID
    atribuicao : ID SLASH EQUALS ID
    atribuicao : ID PERCENT EQUALS ID
    atribuicao : ID AND EQUALS ID
    atribuicao : ID OR EQUALS ID
    expressao : expressao_logica
    expressao_logica : expressao_relacional
    expressao_logica : expressao_logica AND_PALAVRA_RESERVADA expressao_relacional
    expressao_logica : expressao_logica OR_PALAVRA_RESERVADA expressao_relacional
    expressao_logica : NOT expressao_relacional
    expressao_relacional : expressao_aritmetica
    expressao_relacional : expressao_aritmetica GREATER_THAN expressao_aritmetica
    expressao_relacional : expressao_aritmetica GREATER_THAN_EQUAL expressao_aritmetica
    expressao_relacional : expressao_aritmetica LESS_THAN expressao_aritmetica
    expressao_relacional : expressao_aritmetica GREATER_THAN_EQUAL expressao_aritmetica
    expressao_relacional : expressao_aritmetica NOT_EQUAL expressao_aritmetica
    expressao_relacional : expressao_aritmetica DOUBLEEQUALS expressao_aritmetica
    expressao_aritmetica : expressao_multiplicativa
                       | expressao_aritmetica PLUS expressao_multiplicativa
                       | expressao_aritmetica MINUS expressao_multiplicativa
    expressao_multiplicativa : expressao_unaria
                          | expressao_multiplicativa ASTERISC expressao_unaria
                          | expressao_multiplicativa SLASH expressao_unaria
                          | expressao_multiplicativa PERCENT expressao_unaria
    expressao_unaria : expressao_postfix
                   | MINUS expressao_unaria
                   | PLUS expressao_unaria
                   | PLUS PLUS expressao_postfix
                   | MINUS MINUS expressao_postfix
    expressao_postfix : primaria
                   | primaria LBRACKET expressao RBRACKET
                   | primaria LPAREN argumentos RPAREN
                   | primaria DOT ID
                   | primaria ARROW ID
    argumentos : expressao_lista
              | vazio
    primaria : ID
            | NUM_INT
            | NUM_DEC
            | TEXTO
            | LPAREN expressao RPAREN
    expressao_lista : expressao_lista COMMA expressao
                   | expressao
                   | vazio
    '''
def p_comentario(p):
    '''
    comentario : COMMENT
    comentario : COMMENT_MULTI
    '''
def p_tipo(p):
    '''
    tipo : INT_PALAVRA_RESERVADA | FLOAT_PALAVRA_RESERVADA | DOUBLE_PALAVRA_RESERVADA | CHAR_PALAVRA_RESERVADA | BOOLEAN_PALAVRA_RESERVADA
    
    '''



parser = yacc.yacc()
s = Complemento.codigo()
parser.parse(s)
print("sintatico ok")
