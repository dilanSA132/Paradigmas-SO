class Interpretar:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}
        self.results = []  # Almacena los resultados de la ejecución
        self.debug_mode = True  # Habilitar mensajes de depuración

    def evaluate(self):
        for node in self.ast:
            self.execute_statement(node)  # Ejecutar cada nodo del AST
        return self.results  # Retornar todos los resultados al final

    def execute_statement(self, statement):
        stmt_type = statement[0]

        if stmt_type == 'declare':
            _, var_type, var_name, expr = statement
            value = self.evaluate_expression(expr)
            self.check_type(value, var_type)  # Verificar tipo antes de asignar
            self.variables[var_name] = value
            return value

        elif stmt_type == 'declare_vector':
            _, var_name, expr_list = statement
            value_list = [self.evaluate_expression(expr) for expr in expr_list]
            self.variables[var_name] = value_list
            return value_list

        elif stmt_type == 'print':
            self.handle_print(statement)

        elif stmt_type == 'orbit':
            self.handle_orbit(statement)

        elif stmt_type == 'stardock':
            self.handle_stardock(statement)

    def check_type(self, value, expected_type):
        if expected_type == 'int' and not isinstance(value, (int, float)):
            raise TypeError(f"Expected an integer, but got {type(value).__name__}.")
        elif expected_type == 'string' and not isinstance(value, str):
            raise TypeError(f"Expected a string, but got {type(value).__name__}.")

    def handle_print(self, statement):
        if len(statement) == 3:
            _, message, expr = statement
            value = self.evaluate_expression(expr)
            result_message = f"{message}: {value}"
        else:
            _, expr = statement
            value = self.evaluate_expression(expr)
            result_message = f"{value}" if value is not None else f"Variable '{expr[1]}' not defined"

        self.debug_print(result_message)
        self.results.append(result_message)

    def handle_orbit(self, statement):
        _, var_name, start_expr, end_expr, interval_expr, block = statement
        start_value = self.evaluate_expression(start_expr)
        end_value = self.evaluate_expression(end_expr)
        interval_value = self.evaluate_expression(interval_expr)

        if interval_value == 0:
            raise ValueError("Interval cannot be 0.")

        # Iteración en función del valor de inicio y fin
        i = start_value
        if start_value <= end_value:
            while i <= end_value:
                self.variables[var_name] = i
                self.execute_block(block)
                i += interval_value
        else:
            while i >= end_value:
                self.variables[var_name] = i
                self.execute_block(block)
                i -= interval_value

    def execute_block(self, block):
        for stmt in block:
            self.execute_statement(stmt)

    def handle_stardock(self, statement):
        _, condition, true_block, false_block = statement
        condition_value = self.evaluate_expression(condition)

        if condition_value:
            self.execute_block(true_block)
        else:
            self.execute_block(false_block)

    def evaluate_expression(self, expr):
        if isinstance(expr, tuple):
            return self.evaluate_tuple_expression(expr)
        elif isinstance(expr, (int, float, str)):
            return expr
        return None

    def evaluate_tuple_expression(self, expr):
        expr_type = expr[0]

        if expr_type == 'num':
            return expr[1]

        elif expr_type == 'string':
            return expr[1]

        elif expr_type == 'var':
            return self.variables.get(expr[1], None)

        elif expr_type == 'index_access':
            vector_name = expr[1]
            index = self.evaluate_expression(expr[2])
            vector = self.variables.get(vector_name, None)
            if isinstance(vector, list) and 0 <= index < len(vector):
                return vector[index]
            else:
                raise IndexError(f'Index {index} out of bounds for vector {vector_name}')

        # Operadores aritméticos y lógicos
        left = self.evaluate_expression(expr[1])
        right = self.evaluate_expression(expr[2])
        
        if expr_type == 'plus':
            return left + right
        elif expr_type == 'minus':
            return left - right
        elif expr_type == 'times':
            return left * right
        elif expr_type == 'divide':
            if right == 0:
                raise ValueError("Division by zero is not allowed.")
            return left / right
        elif expr_type == 'less':
            return left < right
        elif expr_type == 'greater':
            return left > right
        elif expr_type == 'greatereq':
            return left >= right
        elif expr_type == 'lesseq':
            return left <= right
        elif expr_type == 'equals':
            return left == right
        elif expr_type == 'notequal':
            return left != right
        elif expr_type == 'and':
            return left and right
        elif expr_type == 'or':
            return left or right

        return None

    def debug_print(self, message):
        if self.debug_mode:
            print(f"DEBUG: {message}")  # Imprimir mensajes de depuración solo si están habilitados
