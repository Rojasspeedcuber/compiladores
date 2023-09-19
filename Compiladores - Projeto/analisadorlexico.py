import re

# Definir as expressões regulares para cada tipo de token
patterns = [
    (r'\d+', 'NUM_INT'),                  # Números Inteiros
    (r'\d+\.\d+', 'NUM_DEC'),             # Números Decimais
    (r'[a-zA-Z_]\w*', 'ID'),             # Identificadores
    (r'"[^"]*"', 'TEXTO'),               # Constantes de Texto
    (r'int|float|char|boolean|void|if|else|for|while|scanf|println|main|return', 'PALAVRA_RESERVADA'),  # Palavras Reservadas
    (r'\/\/[^\n]*', 'COMENTARIO'),       # Comentários
    (r'\+|-|\*|\/|%|&&|\|\||!|>|>=|<|<=|!=|==|=|\(|\)|\[|\]|\{|\}|,|;', 'OPERADOR'),  # Operadores e Símbolos Especiais
    (r'\s+', None)                       # Espaços em branco (ignorados)
]

# Função para tokenizar o código-fonte
def tokenize(code):
    tokens = []
    while code:
        for pattern, token_type in patterns:
            match = re.match(pattern, code)
            if match:
                if token_type:
                    tokens.append((match.group(0), token_type))
                code = code[len(match.group(0)):].lstrip()
                break
        else:
            raise SyntaxError(f'Token inválido: {code}')
    return tokens

# Exemplo de código-fonte
codigo_fonte = """
int main() {
    int x = 123;
    float y = 45,67;
    char texto = "Exemplo";
    // Comentário de uma linha
    if (x > 100) {
        println("Maior que 100");
    } else {
        println("Menor ou igual a 100");
    }
    return 0;
}
"""

try:
    tokens = tokenize(codigo_fonte)
    for token in tokens:
        print(token)
except SyntaxError as e:
    print(f'Erro de sintaxe: {e}')
