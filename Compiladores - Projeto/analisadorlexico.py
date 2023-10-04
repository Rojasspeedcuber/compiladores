import re

# Definir as expressões regulares para cada tipo de token
patterns = [
    (r'\d+', 'NUM_INT'),                  # Números Inteiros
    (r'\d+\.\d+', 'NUM_DEC'),             # Números Decimais
    (r'[a-zA-Z_]\w*', 'ID'),             # Identificadores
    (r'"[^"]*"', 'TEXTO'),               # Constantes de Texto
    (r'int|float|char|boolean|void|if|else|for|while|scanf|println|main|return', 'PALAVRA_RESERVADA'),  # Palavras Reservadas
    (r'\/\/[^\n]*', 'COMENTARIO'), # Comentários em uma linha
    (r'\/\*[\s\S]*?\*\/', 'COMENTARIO_MULTI_LINHA'), # Comentários em múltiplas linhas
    (r'\+|-|\*|\/|%|&&|\|\||!|>|>=|<|<=|!=|==|=|\(|\)|\[|\]|\{|\}|.|;', 'OPERADOR'),  # Operadores e Símbolos Especiais
    (r'\s+', None)                       # Espaços em branco (ignorados)
]

# Função para tokenizar o código-fonte
def tokenize(code):
    tokens = []
    while code:
        for pattern, token_type in patterns:
            match = re.match(pattern, code, re.DOTALL)
            if match:
                if token_type:
                    if token_type != 'COMENTARIO_MULTI_LINHA':  # Ignorar comentários de várias linhas
                        tokens.append((match.group(0), token_type))
                code = code[len(match.group(0)):].lstrip()
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
nome_arquivo = 'Compiladores - Projeto\input.txt'
try:
    codigo_fonte = ler_codigo_de_arquivo(nome_arquivo)
    tokens = tokenize(codigo_fonte)
    for token in tokens:
        print(token)
except FileNotFoundError:
    print(f'Arquivo "{nome_arquivo}" não encontrado.')
except SyntaxError as e:
    print(f'Erro de sintaxe: {e}')