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
            ('SUPERNOVA',r'supernova'),
            ('END_SUPERNOVA',r'endSupernova\.'), 
            ('STARPATH', r'starpath'), 
            ('OR', r'or'),
            ('GREATEREQ', r'>='),         
            ('LESSEQ', r'<='),            
            ('GREATER', r'>'),             
            ('LESS', r'<'),                
            ('EQUALS',r'=='),
            ('NOTEQUAL',r'!='),   
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
