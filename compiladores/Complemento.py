TIPOS = [
    'INTEGER_NUMBER',
    'DECIMAL_NUMBER',
    'COMMENT',
    'COMMENT_MULTI',
    'ID',
    'BOOL',
    'STRING',
    'SPECIAL_SYMBOL',
    'OPERATOR'
]


palavras_reservadas = {
    'int': 'INT_PALAVRA_RESERVADA',
    'float': 'FLOAT_PALAVRA_RESERVADA',
    'char': 'CHAR_PALAVRA_RESERVADA',
    'boolean': 'BOOLEAN_PALAVRA_RESERVADA',
    'void': 'VOID_PALAVRA_RESERVADA',
    'if': 'IF_PALAVRA_RESERVADA',
    'else': 'ELSE_PALAVRA_RESERVADA',
    'for': 'FOR_PALAVRA_RESERVADA',
    'while': 'WHILE_PALAVRA_RESERVADA',
    'scanf': 'SCANF_PALAVRA_RESERVADA',
    'println': 'PRINTLN_PALAVRA_RESERVADA',
    'main': 'MAIN_PALAVRA_RESERVADA',
    'return': 'RETURN_PALAVRA_RESERVADA'
}


OPERADORES_E_SIMBOLOS_E = {
    '+': 'PLUS',
    '-': 'MINUS',
    '=': 'EQUALS',
    '*': 'ASTERISC',
    '==': 'DOUBLEEQUALS',
    '/': 'SLASH',  
    '%': 'PERCENT',
    '&&':'AND',
    '||':'OR',  
    '<': 'LESS_THAN',  
    '>': 'GREATER_THAN',  
    '<=': 'LESS_THAN_EQUAL',  
    '>=': 'GREATER_THAN_EQUAL',  
    '!=': 'NOT_EQUAL',
    '!':'NOT',
    '(':'LPAREN',
    ')':'RPAREN',
    '[':'LBRACKET',
    ']':'RBRACKET',
    ',':'COMMA',
    ';':'SEMICOLON'
}
