import re

patterns = [
    (r'\d+', 'NUM_INT'),
    (r'\d+\.\d+', 'NUM_DEC'),
    (r'float|int|char|boolean|void|if|else|for|while|scanf|println|main|return', 'PALAVRA_RESERVADA'),
    (r'[a-zA-Z_]\w*', 'ID'),
    (r'"[^"]*"', 'TEXTO'),
    (r'\/\/[^\n]*', 'COMENTARIO_UMA_LINHA'),
    (r'\/\*[\s\S]*?\*\/', 'COMENTARIO_MULTI_LINHA'),
    (r'\+|-|\*|\/|%|&&|\|\||!|>|>=|<|<=|!=|==|=|\(|\)|\[|\]|\{|\}|.|;', 'OPERADOR'),
    (r'\s+', None)
]

def ler_codigo_de_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        codigo = arquivo.read()
    return codigo

def tokenize(code):
    tokens = []
    while code:
        for pattern, token_type in patterns:
            match = re.match(pattern, code, re.DOTALL)
            if match:
                lexeme = match.group(0)
                if token_type != 'ID':
                    tokens.append((lexeme, token_type))
                code = code[len(lexeme):].lstrip()
                break
        else:
            raise SyntaxError(f'Token inválido: {code}')
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.current_index = 0

    def match(self, expected_type):
        if self.current_token and self.current_token[1] == expected_type:
            token = self.current_token
            self.advance()
            return token
        else:
            raise SyntaxError(f'Erro de sintaxe: esperava {expected_type}, obteve {self.current_token[1]}')

    def advance(self):
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
        else:
            self.current_token = None

    def parse(self):
        self.advance()
        self.program()

    def program(self):
        while self.current_token:
            if self.current_token[1] == 'PALAVRA_RESERVADA':
                if self.current_token[0] in ['int', 'float', 'char', 'boolean', 'void']:
                    self.declaration()
                elif self.current_token[0] == 'if':
                    self.if_statement()
                elif self.current_token[0] == 'for':
                    self.for_loop()
                # Adicione mais casos conforme necessário
            else:
                raise SyntaxError(f'Erro de sintaxe: token inesperado {self.current_token[1]}')

    def declaration(self):
        data_type = self.match('PALAVRA_RESERVADA')
        identifier = self.match('ID')
        # Lógica para processar a declaração
        self.match(';')  # Supondo que cada declaração termina com um ponto e vírgula

    def if_statement(self):
        self.match('PALAVRA_RESERVADA')  # if
        self.match('(')
        # Lógica para processar a condição do if
        self.match(')')
        # Lógica para processar o bloco do if

    def for_loop(self):
        self.match('PALAVRA_RESERVADA')  # for
        self.match('(')
        # Lógica para processar a inicialização, condição e incremento do loop for
        self.match(')')
        # Lógica para processar o bloco do for


nome_arquivo = 'Compiladores - Projeto/input.txt'
try:
    codigo_fonte = ler_codigo_de_arquivo(nome_arquivo)
    tokens = tokenize(codigo_fonte)
    parser = Parser(tokens)
    parser.parse()
    print('Análise sintática bem-sucedida.')
except FileNotFoundError:
    print(f'Arquivo "{nome_arquivo}" não encontrado.')
except SyntaxError as e:
    print(f'Erro de sintaxe: {e}')

