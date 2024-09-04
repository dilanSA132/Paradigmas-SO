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

            if var_type == 'earth' and not isinstance(value, int):
                raise TypeError(f"Expected an integer for variable {var_name}, but got {value}")
            elif var_type == 'mercury' and not isinstance(value, float):
                raise TypeError(f"Expected a float for variable {var_name}, but got {value}")
            elif var_type == 'venus' and not isinstance(value, str):
                raise TypeError(f"Expected a string for variable {var_name}, but got {value}")
            elif var_type == 'mars' and not isinstance(value, bool):
                raise TypeError(f"Expected a boolean for variable {var_name}, but got {value}")
            
            self.variables[var_name] = value

        elif stmt_type == 'print':
            _, message, expr = statement
            value = self.evaluate_expression(expr)
            if value is None:
                value = "None"  
            print(f"{message}: {value}")

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
                if expr[1] not in self.variables:
                    raise NameError(f"Variable '{expr[1]}' is not defined")
                return self.variables.get(expr[1])

            elif expr_type == 'plus':
                return self.evaluate_expression(expr[1]) + self.evaluate_expression(expr[2])

            elif expr_type == 'minus':
                return self.evaluate_expression(expr[1]) - self.evaluate_expression(expr[2])

            elif expr_type == 'times':
                return self.evaluate_expression(expr[1]) * self.evaluate_expression(expr[2])

            elif expr_type == 'divide':
                return self.evaluate_expression(expr[1]) / self.evaluate_expression(expr[2])

        elif isinstance(expr, (int, float, str)):
            return expr

        return None
