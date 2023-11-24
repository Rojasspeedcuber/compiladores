import ply.yacc as yacc
from ply.lex import LexError
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

def t_OPERATOR(t):
    r'\+|-|\*|\/|%|&&|\|\||!|>|>=|<|<=|!=|==|='
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

def t_SPECIAL_SYMBOL(t):
    r'\(|\)|\[|\]|\{|\}|.|;'
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

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('nonassoc', 'EQUALS', 'NOT_EQUAL', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'ASTERISC', 'SLASH', 'PERCENT'),
    ('right', 'UMINUS'),  # Para lidar com operador unário de negação (-)
    ('left', 'INCREMENT', 'DECREMENT')
)

def p_programa(p):
    
    if len(p) == 3:
        p[0] = (p[1], p[2]) 
    else:
        p[0] = None

def p_declaracao(p):
    p[0] = p[1]
  
def p_declaracao_variavel(p):
    if len(p) == 4:
        p[0] = {Complemento.TIPOS: p[1], 'ID': p[2]}  
    elif len(p) == 6:
        p[0] = {Complemento.TIPOS: p[1], 'ID': p[2], 'expressao': p[4]}
    
def p_declaracao_funcao(p):
    p[0] = {
        'tipo': p[1],
        'nome': p[2],
        'parametros': p[4],
        'bloco': p[6]
    }
    
def p_declaracao_estrutura(p):
    '''
    declaracao_estrutura : STRUCT ID LBRACKET declaracao_variavel* RBRACKET SEMICOLON
    '''
    p[0] = ('DECLARACAO_ESTRUTURA', p[2], p[4])
 
def p_parametros(p):
    '''
    parametros : parametro
               | parametro COMMA parametros
    '''
    if len(p) == 2:
        p[0] = [p[1]]  # Um único parâmetro
    else:
        p[0] = [p[1]] + p[3]  # Lista de parâmetros
def p_parametro(p):
    if len(p) == 3:
        p[0] = {'tipo': p[1], 'id': p[2]}  # Parâmetro simples
    elif len(p) == 5:
        p[0] = {'tipo': p[1], 'id': p[2], 'array': True}  # Parâmetro de array
    elif len(p) == 4:
        p[0] = {'tipo': p[1], 'id': p[3], 'variadic': True}  # Parâmetro variádico

def p_binary_operators(p):
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expressions(p):
    '''expression : expression MINUS expression
                  | MINUS expression'''
    if (len(p) == 4):
        p[0] = p[1] - p[3]
    elif (len(p) == 3):
        p[0] = -p[2]


def p_bloco(p):
    '''
    bloco : LBRACKET declaracao_lista RBRACKET
    '''
    p[0] = p[2]  # Atribui a lista de declarações ao bloco
    
def p_declaracao_lista(p):
    '''
    declaracao_lista : declaracao declaracao_lista
                    | empty
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # Concatena a declaração atual com a lista existente
    else:
        p[0] = []  # Lista vazia se não houver declarações

def p_comentario_linha(p):
    '''
    comentario : COMMENT
    '''
    p[0] = ("ComentarioLinha", p[1][2:])
    
def p_comentario_bloco(p):
    '''
    comentario : COMMENT_MULTI
    '''
    p[0] = ("ComentarioBloco", p[1][2:-2])
    
def p_atribuicao(p):
    '''
    atribuicao : ID EQUALS expressao
               | ID PLUS_EQUAL expressao
               | ID MINUS_EQUAL expressao
               | ID TIMES_EQUAL expressao
               | ID DIVIDE_EQUAL expressao
               | ID MOD_EQUAL expressao
               | ID AND_EQUAL expressao
               | ID OR_EQUAL expressao
               | ID EQUALS ID
               | ID PLUS_EQUAL ID
               | ID MINUS_EQUAL ID
               | ID TIMES_EQUAL ID
               | ID DIVIDE_EQUAL ID
               | ID MOD_EQUAL ID
               | ID AND_EQUAL ID
               | ID OR_EQUAL ID
    '''
    p[0] = ('atribuicao', p[1], p[2], p[3])
    
def p_estrutura_controle_if(p):
    '''
    estrutura_controle : IF_PALAVRA_RESERVADA LPAREN expressao RPAREN bloco
                      | IF_PALAVRA_RESERVADA LPAREN expressao RPAREN bloco ELSE_PALAVRA_RESERVADA bloco
    '''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])  # Estrutura de árvore para if sem else
    else:
        p[0] = ('if-else', p[3], p[5], p[7])  # Estrutura de árvore para if com else

def p_estrutura_controle_while(p):
    '''
    estrutura_controle : WHILE_PALAVRA_RESERVADA LPAREN expressao RPAREN bloco
    '''
    p[0] = ('while', p[3], p[5])  # Estrutura de árvore para while

def p_estrutura_controle_for(p):
    '''
    estrutura_controle : FOR_PALAVRA_RESERVADA LPAREN expressao SEMICOLON expressao SEMICOLON expressao RPAREN bloco
    '''
    p[0] = ('for', p[3], p[5], p[7], p[9])  # Estrutura de árvore para for

def p_estrutura_controle_switch(p):
    '''
    estrutura_controle : SWITCH_PALAVRA_RESERVADA LPAREN expressao RPAREN case_lista
    '''
    p[0] = ('switch', p[3], p[5])  # Estrutura de árvore para switch

def p_case_lista(p):
    '''
    case_lista : case_decl case_lista
               | empty
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # Lista de estruturas de árvore para case

def p_case_decl(p):
    '''
    case_decl : CASE_PALAVRA_RESERVADA expressao COLON bloco
              | DEFAULT_PALAVRA_RESERVADA COLON bloco
    '''
    if len(p) == 5:
        p[0] = ('case', p[2], p[4])  # Estrutura de árvore para case
    else:
        p[0] = ('default', p[3])  # Estrutura de árvore para default

def p_estrutura_controle_break(p):
    '''
    estrutura_controle : BREAK_PALAVRA_RESERVADA SEMICOLON
    '''
    p[0] = ('break',)  # Estrutura de árvore para break

def p_estrutura_controle_continue(p):
    '''
    estrutura_controle : CONTINUE_PALAVRA_RESERVADA SEMICOLON
    '''
    p[0] = ('continue',)  # Estrutura de árvore para continue

def p_estrutura_controle_return(p):
    '''
    estrutura_controle : RETURN_PALAVRA_RESERVADA expressao SEMICOLON
    '''
    p[0] = ('return', p[2])  # Estrutura de árvore para return

def p_declaracao_estrutura(p):
    '''
    declaracao_estrutura : STRUCT ID LBRACKET corpo_estrutura RBRACKET SEMICOLON
    '''
    p[0] = ('STRUCT', p[2], p[4])  # Estrutura da árvore sintática para uma declaração de estrutura

def p_corpo_estrutura(p):
    '''
    corpo_estrutura : declaracao_variavel corpo_estrutura
                    | empty
    '''
    if len(p) == 3:
        p[0] = (p[1], p[2])  # Estrutura da árvore sintática para o corpo da estrutura
    else:
        p[0] = None  # Indica um corpo de estrutura vazio

def p_declaracao_estrutura_variavel(p):
    '''
    declaracao_variavel : tipo ID SEMICOLON
                      | tipo ID LBRACKET RBRACKET SEMICOLON
    '''
    p[0] = ('DECLARACAO_VARIAVEL', p[1], p[2], None if len(p) == 4 else 'ARRAY')

def p_array(p):
    '''
    array : ID LBRACKET expressao RBRACKET
          | ID LBRACKET RBRACKET
    '''
    if len(p) == 5:
        p[0] = ('array', p[1], p[3])  # Array com índice
    else:
        p[0] = ('array', p[1], None)  # Array sem índice

def p_array_inicializacao(p):
    '''
    array_inicializacao : LBRACKET expressao_lista RBRACKET
    '''
    p[0] = ('array_inicializacao', p[2])

def p_expressao_lista(p):
    '''
    expressao_lista : expressao
                   | expressao_lista COMMA expressao
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expressao_logica(p):
    '''
    expressao_logica : expressao_relacional
                    | expressao_logica AND expressao_relacional
                    | expressao_logica OR expressao_relacional
                    | NOT expressao_relacional
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '!' and isinstance(p[2], tuple):
        p[0] = ('NOT', p[2])
    else:
        p[0] = (p[2], p[1], p[3])

def p_expressao_relacional(p):
    '''
    expressao_relacional : expressao_aritmetica
                       | expressao_aritmetica LESS_THAN expressao_aritmetica
                       | expressao_aritmetica GREATER_THAN expressao_aritmetica
                       | expressao_aritmetica LESS_THAN_EQUAL expressao_aritmetica
                       | expressao_aritmetica GREATER_THAN_EQUAL expressao_aritmetica
                       | expressao_aritmetica NOT_EQUAL expressao_aritmetica
                       | expressao_aritmetica DOUBLEEQUALS expressao_aritmetica
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_expressao_aritmetica(p):
    '''
    expressao_aritmetica : expressao_multiplicativa
                       | expressao_aritmetica PLUS expressao_multiplicativa
                       | expressao_aritmetica MINUS expressao_multiplicativa
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_expressao_multiplicativa(p):
    '''
    expressao_multiplicativa : expressao_unaria
                         | expressao_multiplicativa ASTERISC expressao_unaria
                         | expressao_multiplicativa SLASH expressao_unaria
                         | expressao_multiplicativa PERCENT expressao_unaria
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_expressao_unaria(p):
    '''
    expressao_unaria : expressao_postfix
                    | MINUS expressao_unaria
                    | PLUS expressao_unaria
                    | INCREMENT expressao_postfix
                    | DECREMENT expressao_postfix
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] in ('-', '+'):
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[1], p[2])

def p_expressao_postfix(p):
    '''
    expressao_postfix : primaria
                    | primaria LBRACKET expressao RBRACKET
                    | primaria LPAREN argumentos RPAREN
                    | primaria DOT ID
                    | primaria ARROW ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '[':
        p[0] = ('ARRAY_ACCESS', p[1], p[3])
    elif p[2] == '(':
        p[0] = ('FUNCTION_CALL', p[1], p[3])
    elif p[2] == '.':
        p[0] = ('DOT', p[1], p[3])
    elif p[2] == '->':
        p[0] = ('ARROW', p[1], p[3])

def p_argumentos(p):
    '''
    argumentos : expressao_lista
              | empty
    '''
    p[0] = p[1] if p[1] is not None else []

def p_primaria(p):
    '''
    primaria : ID
            | NUM_INT
            | NUM_DEC
            | TEXTO
            | LPAREN expressao RPAREN
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = p[2]

def p_empty(p):
    '''
    empty :
    '''
    pass




parser = yacc.yacc()


def parse_input(input_string):
    try:
        return parser.parse(input_string)
    except LexError as e:
        print(f"Erro de léxico: {e}")
    except Exception as e:
        print(f"Erro de análise sintática: {e}")


arquivo = 'compiladores\input.txt'
with open(arquivo, 'r') as file:
    data = file.read()

parse_result = parse_input(data)
