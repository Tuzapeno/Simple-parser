# GRUPO: Arthur Neumann Salerno | Henrique Alves Semmer | Vinicius Teider

import sys


# Definição das estruturas =========================

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value


class TokenCollection:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def current_token(self):
        if self.current >= len(self.tokens):
            return None
        return self.tokens[self.current]

    def move(self):
        self.current += 1

    def peek(self, n=1):
        if self.current + n < len(self.tokens):
            return self.tokens[self.current + n].token_type
        return None

    def expect(self, token_expct):
        token = self.current_token()
        if token is None:
            return False
        if token.token_type != token_expct:
            return False
        return True


# Máquina de estados finitos ===========================

def tokenize_line(line):
    tokens = []
    pos = 0

    while pos < len(line):
        if line[pos] == '(':
            tokens.append(Token('ABREPAREN', line[pos]))
            pos += 1
            
        elif line[pos] == ')':
            tokens.append(Token('FECHAPAREN', line[pos]))
            pos += 1

        elif line[pos] == "\\":
            pos += 1

            if line[pos:].startswith("neg"):
                tokens.append(Token('OPERATORUNARIO', 'neg'))
                pos += len("neg")

            elif line[pos:].startswith("rightarrow"):
                tokens.append(Token('OPERATORBINARIO', 'rightarrow'))
                pos += len("rightarrow")

            elif line[pos:].startswith("leftrightarrow"):
                tokens.append(Token('OPERATORBINARIO', 'leftrightarrow'))
                pos += len("leftrightarrow")

            elif line[pos:].startswith("wedge"):
                tokens.append(Token('OPERATORBINARIO', 'wedge'))
                pos += len("wedge")

            elif line[pos:].startswith("vee"):
                tokens.append(Token('OPERATORBINARIO', 'vee'))
                pos += len("vee")

            else:
                return None

        elif line[pos] == 't' or line[pos] == 'f':

            if line[pos:].startswith('true'):
                tokens.append(Token('CONSTANTE', 'true'))
                pos += len('true')

            elif line[pos:].startswith('false'):
                tokens.append(Token('CONSTANTE', 'false'))
                pos += len('false') 
            else:
                return None
            
        elif line[pos].isnumeric():
            word = line[pos]
            pos += 1
            while pos < len(line) and line[pos].isalnum():
                word += line[pos]
                pos += 1
            tokens.append(Token('PROPOSICAO', word))

        elif line[pos] == ' ':
            pos += 1

        else:
            return None

    return TokenCollection(tokens)


# Funções de parsing ===============================


def parse_formula(tokens):
    token = tokens.current_token()

    match token.token_type:
        case 'CONSTANTE':
            tokens.move()
            return True
        case 'PROPOSICAO':
            tokens.move()
            return True
        case 'ABREPAREN':
            if tokens.peek(1) == 'OPERATORUNARIO':
                return parse_formula_unaria(tokens)
            elif tokens.peek(1) == 'OPERATORBINARIO':
                return parse_formula_binaria(tokens)
            else:
                return False
        case _:
            return False


def parse_formula_unaria(tokens):
    if not tokens.expect('ABREPAREN'):
        return False
    tokens.move()

    if not tokens.expect('OPERATORUNARIO'):
        return False
    tokens.move()

    if not parse_formula(tokens):
        return False

    if not tokens.expect('FECHAPAREN'):
        return False
    tokens.move()

    return True


def parse_formula_binaria(tokens):
    if not tokens.expect('ABREPAREN'):
        return False
    tokens.move()

    if not tokens.expect('OPERATORBINARIO'):
        return False
    tokens.move()

    if not parse_formula(tokens):
        return False

    if not parse_formula(tokens):
        return False

    if not tokens.expect('FECHAPAREN'):
        return False
    tokens.move()

    return True


def test_file(file_name):
    with open(file_name, 'r') as file:
        expression_count = file.readline().strip()
        
        try:
            expression_count = int(expression_count)
        except ValueError:
            print("Primeira linha deve ser um inteiro e deve representar o número de expressões.")
            sys.exit(1)

        lines = file.readlines()

        # Limpar linhas vazias
        for line in lines:
            if not line.strip():
                lines.remove(line)

        if len(lines) != expression_count:
            print(f"Arquivo deve conter {expression_count} expressões, identificadas: {len(lines)}.")
            sys.exit(1)

        for i in range(expression_count):
            line = lines[i].strip()
            if line:
                tokens_obj = tokenize_line(line)
                
                if not tokens_obj:
                    print("Invalida")
                    continue

                value = parse_formula(tokens_obj)

                if value and tokens_obj.current_token() is None:
                    print("Valida")
                else:
                    print("Invalida")


# MAIN ===============================

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)

    file_name = sys.argv[1]

    if not file_name.endswith('.txt'):
        print("Extensão deve ser (.txt)")
        sys.exit(1)

    try:
        test_file(file_name)
    except FileNotFoundError:
        print(f"Arquivo {file_name} não encontrado.")
        sys.exit(1)
