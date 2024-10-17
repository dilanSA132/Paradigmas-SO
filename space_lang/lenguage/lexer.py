import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.token_specification = [
            ('COMMENT', r'#.*'),  # Comentarios
            ('ANDROMEDA', r'andromeda'),  # Nueva palabra reservada para funciones
            ('STARDUST', r'stardust'),  # Nueva palabra reservada para retornar valores
            ('END_ANDROMEDA', r'endAndromeda'),  # Fin de funciones
            ('AND', r'and'),  # Operador lógico and
            
            ('PLANET', r'planet'),  # Declaración de tipos
            ('MERCURY', r'mercury'), # tipo float
            ('VENUS', r'venus'), # tipo string
            ('EARTH', r'earth'), # tipo int 
            ('MARS', r'mars'), # tipo bool
            ('JUPITER', r'jupiter'), # tipo double
            ('CONSTELLATION', r'Constellation'),
            ('STELLAR', r'Stellar'),  # Otros identificadores
            ('ASTRO',r'Astro'), # Pila
            ('NEBULA',r'Nebula'),
            # Nuevos tokens para operaciones en Astro
            ('ASTRO_LAUNCH', r'astro_launch'),  # Añadir elemento
            ('ASTRO_REENTRY', r'astro_reentry'),  # Eliminar 
            ('ASTRO_ORBITTOP', r'astro_orbitTop'),  # Obtener el número tope
            ('ASTRO_ISVACUUM', r'astro_isVacuum'),  # Verificar si esta vacia

            # Nuevos tokens para operaciones en Astro
            ('NEBULA_EVENTHORIZON', r'nebula_eventHorizon'),  # Añadir elemento
            ('NEBULA_LIGHTSPEED', r'nebula_lightSpeed'),  # Eliminar 
            ('NEBULA_CORE', r'nebula_core'),  # Obtener el número tope
            ('NEBULA_ISVACUUM', r'nebula_isVacuum'),  # Verificar si esta vacia
            ('NEBULA_COSMICFLOW',r'nebula_cosmicFlow'),
            
            # Nuevos tokens para operaciones en Stellar
            ('STELLAR_ADD', r'stellar_add'),  # Añadir elemento
            ('STELLAR_REMOVE', r'stellar_remove'),  # Eliminar por índice
            ('STELLAR_SIZE', r'stellar_size'),  # Obtener tamaño
            ('STELLAR_PLACE', r'stellar_place'),  # Insertar en índice

            ('ORBIT', r'orbit'), # Bucle
            ('END_ORBIT', r'endOrbit\.'),   # Fin de bucle
            ('STARDOCK', r'stardock'), # Condicional
            ('END_STARDOCK', r'endStardock\.'), # Fin de condicional
            ('SUPERNOVA', r'supernova'), # Función
            ('END_SUPERNOVA', r'endSupernova\.'), # Fin de función
            ('PERSEIDS', r'perseids'), 
            ('END_PERSEIDS', r'endPerseids\.'),
            ('METEOR', r'meteor'),
            ('END_METEOR', r'endMeteor\.'),
            ('COMMET', r'commet'),
            ('END_COMMET', r'endCommet\.'),
            ('STARPATH', r'starpath'), 
            ('GREATEREQ', r'>='),         
            ('LESSEQ', r'<='),            
            ('GREATER', r'>'),    
            ('OR', r'or'),  # Operador lógico or
            ('LESS', r'<'),                
            ('EQUALS', r'=='),
            ('NOTEQUAL', r'!='), 
            ('TRUE', r'(?i:true)'),  # Manejo de booleanos true y false (insensible a mayúsculas)
            ('FALSE', r'(?i:false)'), 
            ('STRING', r'"[^"]*"'),  # Cadenas
            ('ID', r'[A-Za-z_]\w*'),  # Identificadores
            ('NUMBER', r'\d+\.\d+|\d+'),  # Números
            ('ASSIGN', r'='),  # Asignación
            ('PLUS', r'\+'),  # Suma
            ('MINUS', r'-'),  # Resta
            ('TIMES', r'\*'),  # Multiplicación
            ('DIVIDE', r'/'),  # División
            ('END', r'\.'),  # Fin de una sentencia
            ('COMMA', r','),  # Coma
            ('LPAREN', r'\['),  # Paréntesis izquierdo
            ('RPAREN', r'\]'),  # Paréntesis derecho
            ('COLON', r':'),  # Dos puntos
            ('NEWLINE', r'\n'),  # Nueva línea
            ('SKIP', r'[ \t]+'),  # Espacios y tabulaciones
            ('LCURLYBRACK', r'\{'),  # Llave izquierda
            ('DCURLYBRACK', r'\}'),  # Llave derecha
            ('MISMATCH', r'.'),  # Cualquier otro carácter no esperado
        ]
        self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)

    def tokenize(self):
        """Tokeniza el código fuente dado en la inicialización"""
        line_number = 1
        line_start = 0

        for mo in re.finditer(self.token_regex, self.source_code):
            kind = mo.lastgroup  
            value = mo.group(kind)  

            if kind == 'NEWLINE':
                line_number += 1
                line_start = mo.end()
                continue

            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)  
            elif kind == 'STRING':
                value = value[1:-1]  
            elif kind in ('SKIP', 'COMMENT'):
                continue  
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character "{value}" at line {line_number}')  

            self.tokens.append((kind, value))
        
        return self.tokens

    def get_next_token(self, match_object):
        """Obtiene el siguiente token después del token actual"""
        start = match_object.end()
        next_match = re.search(self.token_regex, self.source_code[start:])
        if next_match:
            return next_match.lastgroup, next_match.group(next_match.lastgroup)
        return None
