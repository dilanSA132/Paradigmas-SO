import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.token_specification = [
            ('COMMENT', r'#.*'),
            ('AND', r'and'),
            ('PLANET', r'planet'),
            ('MERCURY', r'mercury'),
            ('VENUS', r'venus'),
            ('EARTH', r'earth'),
            ('MARS', r'mars'),
            ('JUPITER', r'jupiter'),
            ('STELLAR', r'Stellar'),
            ('ORBIT', r'orbit'),
            ('END_ORBIT', r'endOrbit\.'), 
            ('STARDOCK', r'stardock'),
            ('END_STARDOCK', r'endStardock\.'), 
            ('SUPERNOVA', r'supernova'),
            ('END_SUPERNOVA', r'endSupernova\.'), 
            ('STARPATH', r'starpath'), 
            ('OR', r'or'),
            ('GREATEREQ', r'>='),         
            ('LESSEQ', r'<='),            
            ('GREATER', r'>'),             
            ('LESS', r'<'),                
            ('EQUALS', r'=='),
            ('NOTEQUAL', r'!='),   
            ('STRING', r'"[^"]*"'),
            ('ID', r'[A-Za-z_]\w*'),
            ('NUMBER', r'\d+\.\d+|\d+'),
            ('ASSIGN', r'='),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('TIMES', r'\*'),
            ('DIVIDE', r'/'),
            ('END', r'\.'),
            ('COMMA', r','),
            ('LPAREN', r'\['),  
            ('RPAREN', r'\]'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),   
            ('LCURLYBRACK', r'\{'),          
            ('DCURLYBRACK', r'\}'),        
            ('MISMATCH', r'.'),          
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)

    def tokenize(self):
        line_number = 1
        line_start = 0

        for mo in re.finditer(self.token_regex, self.source_code):
            kind = mo.lastgroup
            value = mo.group(kind)

            # Manejo de nuevas líneas para rastrear errores
            if kind == 'NEWLINE':
                line_number += 1
                line_start = mo.end()
                continue
            
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'STRING':
                value = value[1:-1]  # Eliminar las comillas
            elif kind in ('SKIP', 'COMMENT'):
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character "{value}" at line {line_number}')

            # Manejo de declaración de variables
            if kind == 'PLANET':
                next_token = self.get_next_token(mo)
                if next_token and next_token[0] == 'ID':
                    # Aquí podrías agregar más validaciones según tus reglas
                    self.tokens.append((kind, value))
                    continue
            
            self.tokens.append((kind, value))
        
        return self.tokens

    def get_next_token(self, match_object):
        """Obtiene el siguiente token después del token actual."""
        start = match_object.end()
        next_match = re.search(self.token_regex, self.source_code[start:])
        if next_match:
            return next_match.lastgroup, next_match.group(next_match.lastgroup)
        return None
