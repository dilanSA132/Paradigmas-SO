class Interpretar:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}

    def evaluate(self):
        for node in self.ast:
            self.execute_statement(node)

    def execute_statement(self, statement):
        stmt_type = statement[0]

        if stmt_type == 'declare':
            _, var_type, var_name, expr = statement
            value = self.evaluate_expression(expr)
            self.variables[var_name] = value

        elif stmt_type == 'declare_vector':
            _, var_name, expr_list = statement
            value_list = [self.evaluate_expression(expr) for expr in expr_list]
            self.variables[var_name] = value_list

        elif stmt_type == 'print':
            if len(statement) == 3:  # If both message and expression exist
                _, message, expr = statement
                value = self.evaluate_expression(expr)
                if isinstance(value, list):
                    print(f"{message}: {', '.join(map(str, value))}")
                elif value is None:
                    print(f"{message}: None")
                else:
                    print(f"{message}: {value}")
            else:  # Just print the message
                _, message = statement
                if message == '\\n':
                    print()  # Print a newline
                else:
                    print(message)  # Print the message

        elif stmt_type == 'orbit':
            _, var_name, start_expr, end_expr, interval_expr, block = statement
            start_value = self.evaluate_expression(start_expr)
            end_value = self.evaluate_expression(end_expr)
            interval_value = self.evaluate_expression(interval_expr)

            if interval_value == 0:
                raise ValueError("Intervalo no puede ser 0.")

            if start_value <= end_value:
                i = start_value
                while i <= end_value:
                    self.variables[var_name] = i
                    for stmt in block:
                        self.execute_statement(stmt)
                    i += interval_value  
            else:
                i = start_value
                while i >= end_value:
                    self.variables[var_name] = i
                    for stmt in block:
                        self.execute_statement(stmt)
                    i -= interval_value  

        elif stmt_type == 'stardock':
            _, condition, true_block, false_block = statement
            
            # Evaluar la condición
            condition_value = self.evaluate_expression(condition)
            
            # Si la condición es verdadera, ejecuta el bloque 'if'
            if condition_value:
                for stmt in true_block:
                    self.execute_statement(stmt)
            # Si la condición es falsa, ejecuta el bloque 'else' (si existe)
            else:
                for stmt in false_block:
                    self.execute_statement(stmt)

    def evaluate_expression(self, expr):
        if isinstance(expr, tuple):
            expr_type = expr[0]

            if expr_type == 'num':
                return expr[1]

            elif expr_type == 'string':
                return expr[1]

            elif expr_type == 'var':
                if expr[1] == 'true':
                    return True
                elif expr[1] == 'false':
                    return False
                return self.variables.get(expr[1], None)

            elif expr_type == 'index_access':
                vector_name = expr[1]
                index = self.evaluate_expression(expr[2])  
                vector = self.variables.get(vector_name, None)
                if isinstance(vector, list) and 0 <= index < len(vector):
                    return vector[index]
                else:
                    raise IndexError(f'Index {index} out of bounds for vector {vector_name}')

            elif expr_type == 'plus':
                return self.evaluate_expression(expr[1]) + self.evaluate_expression(expr[2])

            elif expr_type == 'minus':
                return self.evaluate_expression(expr[1]) - self.evaluate_expression(expr[2])

            elif expr_type == 'times':
                return self.evaluate_expression(expr[1]) * self.evaluate_expression(expr[2])

            elif expr_type == 'divide':
                return self.evaluate_expression(expr[1]) / self.evaluate_expression(expr[2])
            
            elif expr_type == 'less':
                return self.evaluate_expression(expr[1]) < self.evaluate_expression(expr[2])

            elif expr_type == 'greater':
                return self.evaluate_expression(expr[1]) > self.evaluate_expression(expr[2])
            
            elif expr_type == 'greatereq':
                return self.evaluate_expression(expr[1]) >= self.evaluate_expression(expr[2])
            
            elif expr_type == 'lesseq':
                return self.evaluate_expression(expr[1]) <= self.evaluate_expression(expr[2])

            elif expr_type == 'equals':
                return self.evaluate_expression(expr[1]) == self.evaluate_expression(expr[2])

            elif expr_type == 'notequal':
                return self.evaluate_expression(expr[1]) != self.evaluate_expression(expr[2])
            
            elif expr_type == 'and':
                return self.evaluate_expression(expr[1]) and self.evaluate_expression(expr[2])
            
            elif expr_type == 'or':
                return self.evaluate_expression(expr[1]) or self.evaluate_expression(expr[2])

        elif isinstance(expr, (int, float, str)):
            return expr

        return None
