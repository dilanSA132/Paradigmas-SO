class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

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
            var_type = self.tokens[self.pos][0]
            self.pos += 1
            var_name = self.tokens[self.pos][1]
            self.pos += 1
            self.pos += 1 
            expr = self.parse_expression()
            self.pos += 1  
            return ('declare', var_type, var_name, expr)

        elif token[0] == 'STELLAR':
            self.pos += 1
            var_name = self.tokens[self.pos][1]
            self.pos += 1  
            self.pos += 1  
            expr_list = self.parse_list()
            self.pos += 1  
            return ('declare_vector', var_name, expr_list)
        
        elif token[0] == 'STARDOCK':
            self.pos += 1
            condition = self.parse_condition() 
            print("LOL "+ condition[0])
            #self.pos += 1 
            block = self.parse_block('END_STARDOCK')
            print("HOLAAA "+self.tokens[self.pos][0])
            if self.tokens[self.pos][0] == 'END': 
                self.pos += 1
            return ('stardock', condition, block)

        elif token[0] == 'ID' and token[1] == 'star':
            self.pos += 1  
            message = self.parse_expression()
            expr = self.parse_expression()
            self.pos += 1  
            return ('print', message, expr)

        elif token[0] == 'ORBIT':
            self.pos += 1  
            var_name = self.tokens[self.pos][1]
            self.pos += 1  
            start_expr = self.parse_expression()
            end_expr = self.parse_expression()
            self.pos += 1  
            block = self.parse_block('END_ORBIT') 
            print(block) 
            return ('orbit', var_name, start_expr, end_expr, block)

        else:
            raise SyntaxError(f'Unexpected token: {token}')

    def parse_block(self, end_token):
        block = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != end_token:
            statement = self.parse_statement()
            if statement:
                block.append(statement)
        if self.tokens[self.pos][0] == end_token:
            self.pos += 1  
        else:
            raise SyntaxError(f"Expected {end_token}, but got {self.tokens[self.pos]}")
        return block

    def parse_condition(self):
        left = self.parse_expression()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('LESS', 'GREATER', 'EQUALS', 'NOTEQUAL','AND','OR'):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.parse_expression()
            left = (op.lower(), left, right)
        if self.tokens[self.pos][0] == 'END':
            self.pos += 1  
        
        return left
    
    def parse_expression(self):
        left = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('PLUS', 'MINUS'):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.parse_term()
            left = (op.lower(), left, right)
        return left

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
        self.pos += 1
        if token[0] == 'NUMBER':
            return ('num', token[1])
        elif token[0] == 'STRING':
            return ('string', token[1])
        elif token[0] == 'ID':
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'LPAREN': 
                self.pos += 1  
                index_expr = self.parse_expression()  
                self.pos += 1  
                return ('index_access', token[1], index_expr)
            return ('var', token[1])
        elif token[0] == 'LPAREN':
            expr = self.parse_expression()
            self.pos += 1  
            return expr
        else:
            raise SyntaxError(f'Invalid expression: {token}')

    def parse_list(self):
        elements = []
        self.pos += 1  
        while self.tokens[self.pos][0] != 'RPAREN':  
            elements.append(self.parse_expression())
            if self.tokens[self.pos][0] == 'COMMA':
                self.pos += 1  
        self.pos += 1  
        return elements
 # type: ignore