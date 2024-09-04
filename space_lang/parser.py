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
            return ('orbit', var_name, start_expr, end_expr, block)

        else:
            raise SyntaxError(f'Unexpected token: {token}')

    def parse_block(self, end_token):
        """Parses a block of code until it finds the end_token (e.g., 'END_ORBIT')"""
        block = []
        while self.tokens[self.pos][0] != end_token:
            statement = self.parse_statement()
            if statement:
                block.append(statement)
        self.pos += 1  
        return block

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
            return ('var', token[1])
        elif token[0] == 'LPAREN':
            expr = self.parse_expression()
            self.pos += 1 
            return expr
        else:
            raise SyntaxError(f'Invalid expression: {token}')
