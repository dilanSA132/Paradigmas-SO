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
                return self.variables.get(expr[1], None)

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