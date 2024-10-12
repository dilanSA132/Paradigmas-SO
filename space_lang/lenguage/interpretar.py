class Interpretar:
    def __init__(self, ast, input_callback):
        self.ast = ast
        self.variables = {}
        self.functions = {}
        self.results = []
        self.debug_mode = True
        self.input_callback = input_callback
        self.current_function = None  

    def evaluate(self):
        for node in self.ast:
            self.execute_statement(node)
        return self.results

    def execute_statement(self, statement):
        stmt_type = statement[0]

        if stmt_type == 'declare':
            _, var_type, var_name, expr = statement
            value = self.evaluate_expression(expr)
            self.check_type_variable(value, var_type)
            self.variables[var_name] = value
            return value

        elif stmt_type == 'declare_vector':
            _, var_name, expr_list = statement
            value_list = [self.evaluate_expression(expr) for expr in expr_list]
            self.variables[var_name] = value_list
            return value_list

        # Operación para agregar un elemento a un vector
        elif stmt_type == 'stellar_add':
            _, vector_name, element = statement
            element_value = self.evaluate_expression(element)
            self.stellar_append(vector_name, element_value)
            return

        # Operación para remover un elemento de un vector por índice
        elif stmt_type == 'stellar_remove':
            _, vector_name, index = statement
            index_value = self.evaluate_expression(index)
            self.stellar_delete_by_index(vector_name, index_value)
            return

        # Operación para obtener el tamaño de un vector
        elif stmt_type == 'stellar_size':
            _, vector_name = statement
            size = self.stellar_length(vector_name)
            self.debug_print(f"Size of '{vector_name}': {size}")
            self.results.append(f"Size of '{vector_name}': {size}")
            return size

        # Operación para insertar un elemento en un índice específico de un vector
        elif stmt_type == 'stellar_place':
            _, vector_name, index, element = statement
            index_value = self.evaluate_expression(index)
            element_value = self.evaluate_expression(element)
            self.stellar_insert(vector_name, index_value, element_value)
            return

        elif stmt_type == 'print':
            self.handle_print(statement)

        elif stmt_type == 'starcatch':
            _, var_name = statement
            var_type = self.get_variable_type(var_name)
            value = self.input_callback(f"Enter a value for {var_name}: ")
            value = self.convert_value(value, var_type)
            self.variables[var_name] = value
            self.debug_print(f"Captured input for {var_name} ({var_type}): {value}")
            self.results.append(f"Input captured for {var_name}: {value}")

        elif stmt_type == 'orbit':
            self.handle_orbit(statement)

        elif stmt_type == 'stardock':
            self.handle_stardock(statement)

        elif stmt_type == 'perseids':
            self.handle_parseids(statement)

        elif stmt_type == 'function':  
            _, return_type, function_name, parameters, block = statement
            self.functions[function_name] = {
                'return_type': return_type,
                'parameters': parameters,
                'block': block
            }
            self.debug_print(f"Function {function_name} defined with return type {return_type}")

        elif stmt_type == 'call_function': 
            function_name = statement[1]
            args = statement[2]
            return self.call_function(function_name, args)

        elif stmt_type == 'return': 
            return_value = self.evaluate_expression(statement[1])
            self.debug_print(f"Returning value {return_value}")
            return return_value  
        
    def call_function(self, function_name, args):
        if function_name in self.variables:  # Si es un vector o una variable, no debe ser tratado como función
            raise TypeError(f"'{function_name}' is not a function, but a variable.")

        if function_name not in self.functions:
            raise NameError(f"Function {function_name} is not defined.")

        function_info = self.functions[function_name]
        parameters = function_info['parameters']
        block = function_info['block']

        if len(parameters) != len(args):
            raise TypeError(f"Function {function_name} expected {len(parameters)} arguments, got {len(args)}")

        local_vars = {}
        for param, arg in zip(parameters, args):
            param_type, param_subtype, param_name = param
            arg_value = self.evaluate_expression(arg)
            self.check_type(arg_value, param_subtype)
            local_vars[param_name] = arg_value

        previous_vars = self.variables.copy()
        self.variables.update(local_vars)
        return_value = self.execute_block(block)  
        self.variables = previous_vars  
        if return_value is None:
            raise ValueError(f"Function {function_name} did not return a value.")
        
        self.check_type(return_value, function_info['return_type'])
        return return_value

    def get_variable_type(self, var_name):
        """Determina el tipo de la variable basada en el prefijo del tipo (earth, mercury, venus, etc.)."""
        for var_type in ['earth', 'mercury', 'jupiter', 'venus', 'mars']:
            if f"{var_type} {var_name}" in self.variables:
                return var_type
        return None

    def convert_value(self, value, var_type):
        """Convierte el valor de entrada según el tipo de la variable."""
        try:
            if var_type == 'earth': 
                return int(value)
            elif var_type == 'mercury' or var_type == 'jupiter':
                return float(value)
            elif var_type == 'venus': 
                return str(value)
            elif var_type == 'mars': 
                return value.lower() == 'true'
        except ValueError:
            raise TypeError(f"Cannot convert value '{value}' to {var_type}.")
        return value

    def check_type_variable(self, value, expected_type):
        """Verifica si el valor es del tipo esperado."""
        type_map = {
            'EARTH': int,
            'MERCURY': float,
            'JUPITER': float,
            'VENUS': str,
        }
        if expected_type in type_map:
            if not isinstance(value, type_map[expected_type]):
                raise TypeError(f"Expected {type_map[expected_type].__name__}, but got {type(value).__name__}.")
        elif expected_type == 'MARS':
            if value is None:
                raise TypeError("Expected a boolean, but got None.")
            elif isinstance(value, str) and value.lower() in ['true', 'false']:
                value = True if value.lower() == 'true' else False
            elif not isinstance(value, bool):
                raise TypeError(f"Expected a boolean (true/false), but got {type(value).__name__}.")
        else:
            raise TypeError(f"Unknown type '{expected_type}' for validation.")
        
    def check_type(self, value, expected_type):
        """Validar el tipo del valor basado en el tipo esperado."""
        type_map = {
            'EARTH': int,
            'MERCURY': float,
            'JUPITER': float,
            'VENUS': str,
            'MARS': bool,
        }
        if expected_type in type_map and not isinstance(value, type_map[expected_type]):
            raise TypeError(f"Expected {type_map[expected_type].__name__}, but got {type(value).__name__}.")

    # Funciones para el manejo de Stellar (vector)
    def stellar_append(self, vector_name, element):
        if vector_name not in self.variables:
            raise NameError(f"Vector '{vector_name}' is not defined.")
        self.variables[vector_name].append(element)
        self.debug_print(f"Element {element} added to vector '{vector_name}'")

    def stellar_delete_by_index(self, vector_name, index):
        if vector_name not in self.variables:
            raise NameError(f"Vector '{vector_name}' is not defined.")
        if index < 0 or index >= len(self.variables[vector_name]):
            raise IndexError(f"Index {index} out of bounds for vector '{vector_name}'.")
        element = self.variables[vector_name].pop(index)
        self.debug_print(f"Element {element} at index {index} removed from vector '{vector_name}'")

    def stellar_length(self, vector_name):
        if vector_name not in self.variables:
            raise NameError(f"Vector '{vector_name}' is not defined.")
        return len(self.variables[vector_name])

    def stellar_insert(self, vector_name, index, element):
        if vector_name not in self.variables:
            raise NameError(f"Vector '{vector_name}' is not defined.")
        if index < 0 or index > len(self.variables[vector_name]):
            raise IndexError(f"Index {index} out of bounds for vector '{vector_name}'.")
        self.variables[vector_name].insert(index, element)
        self.debug_print(f"Element {element} inserted at index {index} in vector '{vector_name}'")

    def handle_print(self, statement):
        if len(statement) == 3:
            _, message, expr = statement
            message_text = message[1] if message[0] == 'string' else str(self.evaluate_expression(message))
            value = self.evaluate_expression(expr)
            result_message = f"{message_text}: {value}"
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

    def handle_parseids(self, statement):
        _, var_name, cases, default_case = statement
        var_value = self.variables.get(var_name)

        if var_value in cases:
            self.execute_block(cases[var_value])
        elif default_case is not None:
            self.execute_block(default_case)
        else:
            self.debug_print(f"No matching case found for {var_name} with value {var_value}, and no default case provided.")

    def execute_block(self, block):
        return_value = None
        for stmt in block:
            return_value = self.execute_statement(stmt)
            if return_value is not None: 
                return return_value
        return return_value

    def handle_stardock(self, statement):
        _, condition, true_block, false_block = statement
        condition_value = self.evaluate_expression(condition)
        
        if condition_value:
            self.execute_block(true_block)
        else:
            self.execute_block(false_block)
            
    def evaluate_expression(self, expr):
        expr_type = expr[0]

        if expr_type == 'num':
            return expr[1]

        elif expr_type == 'string':
            return expr[1]

        elif expr_type == 'bool':
            return expr[1]

        elif expr_type == 'var':
            var_name = expr[1]
            if var_name not in self.variables:
                raise NameError(f"Variable '{var_name}' is not defined.")
            return self.variables[var_name]

        elif expr_type == 'call_function':
            function_name = expr[1]
            args = expr[2]
            if function_name in self.variables:  # Si es una variable como un vector
                vector = self.variables[function_name]
                index = self.evaluate_expression(args[0])
                if not isinstance(index, int) or index < 0 or index >= len(vector):
                    raise IndexError(f"Index {index} out of bounds for vector {function_name}.")
                return vector[index]  # Acceso al vector por índice
            return self.call_function(function_name, args)

        left = self.evaluate_expression(expr[1])
        right = self.evaluate_expression(expr[2])

        # Operaciones aritméticas y booleanas
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
            print(f"DEBUG: {message}")
