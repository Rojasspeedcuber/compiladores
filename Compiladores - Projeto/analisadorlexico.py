import re

patterns = [
    (r'\d+', 'NUM_INT'),
    (r'\d+\.\d+', 'NUM_DEC'),
    (r'[a-zA-Z_]\w*', 'ID'),
    (r'"[^"]*"', 'TEXTO'),
    (r'int|float|char|boolean|void|if|else|for|while|scanf|println|main|return', 'PALAVRA_RESERVADA'),
    (r'\/\/[^\n]*', 'COMENTARIO_UMA_LINHA'),
    (r'\/\*[\s\S]*?\*\/', 'COMENTARIO_MULTI_LINHA'),
    (r'\+|-|\*|\/|%|&&|\|\||!|>|>=|<|<=|!=|==|=|\(|\)|\[|\]|\{|\}|.|;', 'OPERADOR'),
    (r'\s+', None)
]

def tokenize(code):
    tokens = []
    while code:
        for pattern, token_type in patterns:
            match = re.match(pattern, code, re.DOTALL)
            if match:
                lexeme = match.group(0)
                if token_type == 'ID' and lexeme == 'length':
                    raise SyntaxError('"length" não é permitido.')
                if token_type != 'COMENTARIO_MULTI_LINHA':
                    tokens.append((lexeme, token_type))
                code = code[len(lexeme):].lstrip()
                break
        else:
            raise SyntaxError(f'Token inválido: {code}')
    return tokens

# Função para ler código-fonte de um arquivo
def ler_codigo_de_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        codigo = arquivo.read()
    return codigo

# Ler código-fonte de um arquivo chamado "input.txt"
nome_arquivo = 'input.txt'
try:
    codigo_fonte = ler_codigo_de_arquivo(nome_arquivo)
    tokens = tokenize(codigo_fonte)
    for token in tokens:
        print(token)
except FileNotFoundError:
    print(f'Arquivo "{nome_arquivo}" não encontrado.')
except SyntaxError as e:
    print(f'Erro de sintaxe: {e}')
