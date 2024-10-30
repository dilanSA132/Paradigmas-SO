class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_function = None

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

    def parse_statement(self):
        token = self.tokens[self.pos]

        if token[0] == 'NEWLINE':
            self.pos += 1
            return None

        if token[0] == 'PLANET':
            self.pos += 1
            var_type = self.tokens[self.pos][0].lower()  # Captura el tipo de destino
            self.pos += 1
            var_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'ASSIGN':
                self.pos += 1
                expr = self.parse_expression(var_type=var_type)  # Pasa el tipo de destino a la expresión

                if self.tokens[self.pos][0] == 'END':
                    self.pos += 1
                return ('assign', var_type, var_name, expr)  # Retorna el nodo de asignación
        
        elif token[0] == 'CONSTELLATION':
            self.pos += 1
            var_name = self.tokens[self.pos][1]
            self.pos += 1
            self.pos += 1  
            expr_list = self.parse_list()
            self.pos += 1  
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1  
            return ('declare_vector', var_name, expr_list)
        
        elif token[0] == 'STELLAR':
            self.pos += 1  
            var_name = self.tokens[self.pos][1]  
            self.pos += 1  
            if self.tokens[self.pos][0] == 'ASSIGN': 
                self.pos += 1 
                expr_list = self.parse_list()  
                self.pos += 1 
                return ('declare_vector', var_name, expr_list)

        elif token[0] == 'ASTRO':
            self.pos += 1  
            var_name = self.tokens[self.pos][1]  
            self.pos += 1 
            if self.tokens[self.pos][0] == 'ASSIGN':  
                self.pos += 1  
                expr_list = self.parse_list()  
                self.pos += 1  
                return ('declare_vector', var_name, expr_list)
            
        elif token[0] == 'ASTRO_LAUNCH':
            self.pos += 1
            stack_name = self.tokens[self.pos][1]
            self.pos += 1
            element = self.parse_expression()  
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('astro_launch', stack_name, element)

        elif token[0] == 'ASTRO_REENTRY':
            self.pos += 1
            stack_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('astro_reentry', stack_name)
        
        elif token[0] == 'ASTRO_ORBITTOP':
            self.pos += 1
            stack_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            print('astro_orbittop', stack_name)
            return ('astro_orbittop', stack_name)

        elif token[0] == 'ASTRO_ISVACUUM':
            self.pos += 1
            stack_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('astro_isvacuum', stack_name)
        
        elif token[0] == 'ASTRO_COUNT':
            self.pos += 1
            stack_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('astro_count', stack_name)
        
        elif token[0] == 'NEBULA':
            self.pos += 1  
            var_name = self.tokens[self.pos][1]  
            self.pos += 1 
            if self.tokens[self.pos][0] == 'ASSIGN':  
                self.pos += 1  
                expr_list = self.parse_list()  
                self.pos += 1  
                return ('declare_vector', var_name, expr_list)
            
        elif token[0] == 'NEBULA_EVENTHORIZON':
            self.pos += 1
            queue_name = self.tokens[self.pos][1]
            self.pos += 1
            element = self.parse_expression()  
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('nebula_eventhorizon', queue_name, element)

        elif token[0] == 'NEBULA_LIGHTSPEED':
            self.pos += 1
            queue_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('nebula_lightspeed', queue_name)
        
        elif token[0] == 'NEBULA_CORE':
            self.pos += 1
            queue_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('nebula_core', queue_name)

        elif token[0] == 'NEBULA_ISVACUUM':
            self.pos += 1
            queue_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('nebula_isvacuum', queue_name)
        
        elif token[0] == 'NEBULA_COSMICFLOW':
            self.pos += 1
            queue_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('nebula_cosmicflow', queue_name)
        
        elif token[0] == 'STELLAR_ADD':
            self.pos += 1
            vector_name = self.tokens[self.pos][1]
            self.pos += 1
            element = self.parse_expression()  
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('stellar_add', vector_name, element)

        elif token[0] == 'STELLAR_REMOVE':
            self.pos += 1
            vector_name = self.tokens[self.pos][1]
            self.pos += 1
            index = self.parse_expression()
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('stellar_remove', vector_name, index)
        
        elif token[0] == 'STELLAR_SIZE':
            self.pos += 1
            vector_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('stellar_size', vector_name)

        elif token[0] == 'STELLAR_PLACE':
            self.pos += 1
            vector_name = self.tokens[self.pos][1]
            self.pos += 1
            index = self.parse_expression()  
            element = self.parse_expression()  
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
            return ('stellar_place', vector_name, index, element)

        elif token[0] == 'STARDUST':  
            self.pos += 1  
            expr = self.parse_expression()  
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1 
            return ('return', expr)

        elif token[0] == 'ANDROMEDA': 
            self.pos += 1 
            return_type = self.tokens[self.pos][0]  
            self.pos += 1
            function_name = self.tokens[self.pos][1]  
            self.pos += 1
            self.pos += 1  
            parameters = self.parse_parameters()  
            self.pos += 1 

            if self.tokens[self.pos][0] != 'COLON':
                raise SyntaxError(f"Expected ':', but got {self.tokens[self.pos]} at position {self.pos}")
            
            self.pos += 1 

            block = self.parse_block('END_ANDROMEDA')  
            return ('function', return_type, function_name, parameters, block)

        elif token[0] == 'STARDOCK':
            self.pos += 1
            condition = self.parse_condition()
            self.pos += 1  
            true_block = self.parse_block('END_STARDOCK')
            false_block = []

            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'SUPERNOVA':
                self.pos += 1
                self.pos += 1 
                false_block = self.parse_block('END_SUPERNOVA')

            return ('stardock', condition, true_block, false_block)

        elif token[0] == 'ID' and token[1] == 'star':
            self.pos += 1  
            message = self.parse_expression()
            if self.tokens[self.pos][0] == 'COLON':
                self.pos += 1  
            if self.tokens[self.pos][0] != 'END':
                expr = self.parse_expression()
                self.pos += 1  
                return ('print', message, expr)
            else:
                self.pos += 1  
                return ('print', message)

        elif token[0] == 'ID' and token[1] == 'starcatch':
            self.pos += 1  
            if self.tokens[self.pos][0] == 'STRING':
                message = self.tokens[self.pos][1]
                self.pos += 1
            else:
                message = ""
            var_name = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'END':
                self.pos += 1
                return ('starcatch', message, var_name)
            else:
                raise SyntaxError(f"Expected end of statement but got {self.tokens[self.pos]}")

        elif token[0] == 'ORBIT':
            self.pos += 1
            var_name = self.tokens[self.pos][1]
            self.pos += 1
            start_expr = self.parse_expression()
            end_expr = self.parse_expression()
            interval_expr = self.parse_expression()
            self.pos += 1  
            block = self.parse_block('END_ORBIT')
            print(block)
            return ('orbit', var_name, start_expr, end_expr, interval_expr, block)

        elif token[0] == 'PERSEIDS':
            self.pos += 1
            var_name = self.tokens[self.pos][1]
            self.pos += 1
            cases = {}
            default_case = None
            self.pos += 1
            cases, default_case = self.parse_cases()
            return ('perseids', var_name, cases, default_case)
        
        elif token[0] == 'MOON': 
            self.pos += 1
            function_name = self.tokens[self.pos][1] 
            self.pos += 1
            if self.tokens[self.pos][0] == 'LPAREN': 
                self.pos += 1
                parameters = self.parse_parameters()  
                if self.tokens[self.pos][0] != 'RPAREN': 
                    raise SyntaxError(f"Expected ']', but got {self.tokens[self.pos]} at position {self.pos}")
                self.pos += 1 
            else:
                parameters = [] 

            if self.tokens[self.pos][0] != 'COLON':  
                raise SyntaxError(f"Expected ':', but got {self.tokens[self.pos]} at position {self.pos}")
            self.pos += 1  

            block = self.parse_block('END_MOON')  
            return ('void_function', function_name, parameters, block)

        elif token[0] == 'SUN':  
            self.pos += 1
            function_name = self.tokens[self.pos][1] 
            self.pos += 1
            if self.tokens[self.pos][0] == 'LPAREN': 
                self.pos += 1
                args = self.parse_arguments() 
                if self.tokens[self.pos][0] != 'RPAREN': 
                    raise SyntaxError(f"Expected ']', but got {self.tokens[self.pos]} at position {self.pos}")
                self.pos += 1  
            else:
                args = []  

            if self.tokens[self.pos][0] == 'END': 
                self.pos += 1  
            else:
                raise SyntaxError(f"Expected '.', but got {self.tokens[self.pos]} at position {self.pos}")

            return ('call_void_function', function_name, args)

        else:
            raise SyntaxError(f'Unexpected token: {token} at position {self.pos}')
                        
    def is_casting_required(self, var_type, expr):
        """ Verifica si es necesario realizar un cast de tipo """
        expr_type = self.get_expression_type(expr)
        return var_type != expr_type 

    def get_expression_type(self, expr):
        """ Obtiene el tipo de una expresión """
        if expr[0] == 'num':
            return 'earth'
        elif expr[0] == 'string':
            return 'venus'
        return None
    
    def parse_block(self, end_token):
        """Procesa un bloque de código que termina con un token específico"""
        block = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != end_token:
            statement = self.parse_statement()
            if statement:
                block.append(statement)
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == end_token:
            self.pos +=1

        return block

    def parse_cases(self):
        cases = {}
        default_case = None

        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != 'END_PERSEIDS':
            case_token = self.tokens[self.pos]

            if case_token[0] == 'METEOR':
                self.pos += 1
                case_value = self.tokens[self.pos][1]
                self.pos += 1
                if self.tokens[self.pos][0] == 'END':
                    self.pos += 1
                block = self.parse_block('END_METEOR')
                cases[case_value] = block

            elif case_token[0] == 'COMMET':
                self.pos += 1
                if self.tokens[self.pos][0] == 'END':
                    self.pos += 1
                default_case = self.parse_block('END_COMMET')

            else:
                raise SyntaxError(f"Unexpected token in perseids: {case_token} at position {self.pos}")

        self.pos += 1
        return cases, default_case
    
    def parse_parameters(self):
        parameters = []
        
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != 'RPAREN':
            param_type = self.tokens[self.pos][0]
            self.pos += 1
            
            if param_type == 'STELLAR':
                param_name = self.tokens[self.pos][1]
                self.pos += 1
                parameters.append((param_type, None, param_name))
            
            elif self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('MERCURY', 'VENUS', 'EARTH', 'MARS', 'JUPITER'):
                param_subtype = self.tokens[self.pos][0]
                self.pos += 1
                
                if self.pos >= len(self.tokens):  
                    raise SyntaxError(f"Unexpected end of input, expected parameter name after {param_subtype}")
                
                param_name = self.tokens[self.pos][1]  
                self.pos += 1
                
                parameters.append((param_type, param_subtype, param_name))
            
            else:
                raise SyntaxError(f"Expected a subtype like 'earth' or 'Stellar' after {param_type}, but got {self.tokens[self.pos]}")
            
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'COMMA':
                self.pos += 1  
            elif self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'RPAREN':
                break
            else:
                raise SyntaxError(f"Expected ',' or ']', but got {self.tokens[self.pos]} at position {self.pos}")
        
        return parameters


    def parse_condition(self):
        left = self.parse_expression()
        while (self.pos < len(self.tokens) and 
               self.tokens[self.pos][0] in ('LESS', 'GREATER', 'EQUALS', 'NOTEQUAL', 'AND', 'OR', 'LESSEQ', 'GREATEREQ')):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.parse_expression()
            left = (op.lower(), left, right)
        return left
    
    def parse_expression(self, var_type=None):
        if self.tokens[self.pos][0] == 'NEXTPLANET':
            self.pos += 1
            if self.tokens[self.pos][0] == 'LPAREN':
                self.pos += 1
                expr = self.parse_expression() 
                if self.tokens[self.pos][0] != 'RPAREN':
                    raise SyntaxError(f"Expected ']', but got {self.tokens[self.pos]}")
                self.pos += 1
                target_type = var_type 
                if target_type is None:
                    raise SyntaxError("Target type for nextPlanet casting is not specified.")
                return ('cast', target_type, expr)  

        left = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('PLUS', 'MINUS'):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.parse_term()
            left = (op.lower(), left, right)
        return left

    
    def get_current_var_type(self):
        """Obtener el tipo de la variable a la que se está asignando, si es aplicable"""
        if self.pos > 1 and self.tokens[self.pos - 2][0] == 'PLANET':
            return self.tokens[self.pos - 1][0].lower() 
        return None



    def parse_term(self):
        left = self.parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('TIMES', 'DIVIDE'):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.parse_factor()
            left = (op.lower(), left, right)
        return left
    
    def parse_factor(self):
        token = self.tokens[self.pos]
        if token[0] == 'MINUS':
            self.pos += 1
            next_token = self.tokens[self.pos]
            if next_token[0] == 'NUMBER':
                self.pos += 1
                return ('num', -int(next_token[1]))
            else:
                raise SyntaxError(f"Expected a number after '-', but got {next_token} at position {self.pos}")
        self.pos += 1
        if token[0] == 'NUMBER':
            return ('num', token[1])
        elif token[0] == 'STRING':
            return ('string', token[1])
        elif token[0] == 'TRUE' or token[0] == 'FALSE':
            return ('bool', token[1].lower())
        elif token[0] == 'ID':
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'LPAREN':
                self.pos += 1 
                args = self.parse_arguments() 
                self.pos += 1 
                return ('call_function', token[1], args) 
            return ('var', token[1])
        elif token[0] == 'STELLAR_SIZE':  
            vector_name = self.tokens[self.pos][1]
            self.pos += 1
            return ('stellar_size', vector_name)
        elif token[0] == 'ASTRO_ISVACUUM': 
            stack_name = self.tokens[self.pos][1]
            self.pos += 1
            return ('astro_isvacuum', stack_name)
        
        elif token[0] == 'ASTRO_COUNT':
            stack_name = self.tokens[self.pos][1]
            self.pos += 1
            return ('astro_count', stack_name)
        
        elif token[0] == 'NEBULA_ISVACUUM': 
            queue_name = self.tokens[self.pos][1]
            self.pos += 1
            return ('nebula_isvacuum', queue_name)
        elif token[0] == 'NEBULA_COSMICFLOW': 
            queue_name = self.tokens[self.pos][1]
            self.pos += 1
            return ('nebula_cosmicflow', queue_name)
        
        elif token[0] == 'LPAREN':
            expr = self.parse_expression()
            self.pos += 1  
            return expr
        else:
            raise SyntaxError(f'Invalid expression: {token} at position {self.pos}')

    def parse_arguments(self):
        args = []
        while self.tokens[self.pos][0] != 'RPAREN': 
            args.append(self.parse_expression())
            if self.tokens[self.pos][0] == 'COMMA':  
                self.pos += 1  
        return args

    def parse_list(self):
        elements = []
        if self.tokens[self.pos][0] == 'LPAREN': 
            self.pos += 1 
        while self.tokens[self.pos][0] != 'RPAREN':  
            elements.append(self.parse_expression())  
            if self.tokens[self.pos][0] == 'COMMA':  
                self.pos += 1
        self.pos += 1  
        return elements
