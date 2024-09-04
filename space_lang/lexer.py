import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.token_specification = [
            ('COMMENT', r'#.*'),            # Comentarios
            ('PLANET', r'planet'),          # Declaración de tipo de dato
            ('MERCURY', r'mercury'),        # float
            ('VENUS', r'venus'),            # string
            ('EARTH', r'earth'),            # int
            ('MARS', r'mars'),              # bool
            ('JUPITER', r'jupiter'),        # double
            ('ORBIT', r'orbit'),            # Ciclo for
            ('END_ORBIT', r'endOrbit\.'),   # Fin del ciclo 'orbit' con punto
            ('STRING', r'"[^"]*"'),         # Cadenas de texto
            ('ID', r'[A-Za-z_]\w*'),        # Identificadores
            ('NUMBER', r'\d+\.\d+|\d+'),    # Números (float/int)
            ('ASSIGN', r'='),               # Asignación
            ('PLUS', r'\+'),                # Suma
            ('MINUS', r'-'),                # Resta
            ('TIMES', r'\*'),               # Multiplicación
            ('DIVIDE', r'/'),               # División
            ('END', r'\.'),                 # Fin de instrucción
            ('COMMA', r','),                # Coma
            ('LPAREN', r'\('),              # Paréntesis izquierdo
            ('RPAREN', r'\)'),              # Paréntesis derecho
            ('NEWLINE', r'\n'),             # Fin de línea
            ('SKIP', r'[ \t]+'),            # Espacios en blanco
            ('MISMATCH', r'.'),             # Caracteres no reconocidos
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)

    def tokenize(self):
        for mo in re.finditer(self.token_regex, self.source_code):
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'STRING':
                value = value[1:-1]
            elif kind in ('SKIP', 'COMMENT'):
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character: {value}')
            self.tokens.append((kind, value))
        return self.tokens
