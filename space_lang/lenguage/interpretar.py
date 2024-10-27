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

        if stmt_type == 'assign': 
            _, var_type, var_name, expr = statement
            value = self.evaluate_expression(expr)

            value_type = self.get_type_from_value(value)
            if var_type != value_type:
                if expr[0] == 'cast':
                    value = self.cast_value(value, var_type)  
                else:
                    raise TypeError(f"Cannot assign value of type {value_type} to variable of type {var_type} without explicit casting using nextPlanet.")

            self.variables[var_name] = value  
            self.debug_print(f"Variable '{var_name}' assigned with value: {value}")
            return value



        elif stmt_type == 'declare_vector':
            _, var_name, expr_list = statement
            value_list = [self.evaluate_expression(expr) for expr in expr_list]
            self.variables[var_name] = value_list
            return value_list

        elif stmt_type == 'astro_launch':
            _, list_name, element = statement
            element_value = self.evaluate_expression(element)
            self.astro_append(list_name, element_value)
            return

        elif stmt_type == 'astro_reentry':
            _, list_name = statement

            self.astro_delete_top(list_name)
            return 

        elif stmt_type == 'astro_orbittop':
            _, list_name = statement
            top = self.astro_top(list_name)
            self.debug_print(f"Value top of '{list_name}': {top}")
            self.results.append(f"Value top of '{list_name}': {top}")
            return top

        elif stmt_type == 'astro_isvacuum':
            _, list_name = statement
            return self.astro_is_vacuum(list_name)

        elif stmt_type == 'astro_count':
            _, list_name = statement
            size = self.astro_length(list_name)
            self.debug_print(f"Size of '{list_name}': {size}")
            self.results.append(f"Size of '{list_name}': {size}")
            return size

        elif stmt_type == 'nebula_eventhorizon':
            _, list_name, element = statement
            element_value = self.evaluate_expression(element)
            self.nebula_append(list_name, element_value)
            return
        
        elif stmt_type == 'nebula_lightspeed':
            _, list_name = statement
            self.nebula_delete_front(list_name)
            return 
        
        elif stmt_type == 'nebula_core':
            _, list_name = statement
            front = self.nebula_front(list_name)
            self.debug_print(f"Value front of '{list_name}': {front}")
            self.results.append(f"Value front of '{list_name}': {front}")
            return front
        
        elif stmt_type == 'nebula_isvacuum':
            _, list_name = statement
            return self.astro_is_vacuum(list_name)

        elif stmt_type == 'nebula_cosmicflow':
            _, list_name = statement
            size = self.nebula_length(list_name)
            self.debug_print(f"Size of '{list_name}': {size}")
            self.results.append(f"Size of '{list_name}': {size}")
            return size

        elif stmt_type == 'stellar_add':
            _, vector_name, element = statement
            element_value = self.evaluate_expression(element)
            self.stellar_append(vector_name, element_value)
            return

        elif stmt_type == 'stellar_remove':
            _, vector_name, index = statement
            index_value = self.evaluate_expression(index)
            self.stellar_delete_by_index(vector_name, index_value)
            return

        elif stmt_type == 'stellar_size':
            _, vector_name = statement
            size = self.stellar_length(vector_name)
            self.debug_print(f"Size of '{vector_name}': {size}")
            self.results.append(f"Size of '{vector_name}': {size}")
            return size

        elif stmt_type == 'stellar_place':
            _, vector_name, index, element = statement
            index_value = self.evaluate_expression(index)
            element_value = self.evaluate_expression(element)
            self.stellar_insert(vector_name, index_value, element_value)
            return

        elif stmt_type == 'print':
            self.handle_print(statement)

        elif stmt_type == 'starcatch':
            _, message, var_name = statement
            
            var_type = self.get_variable_type(var_name)
            prompt_message = message if message else f"Enter a value for {var_name}: "
            
            value = self.input_callback(prompt_message)
            
            if value is None:
                raise ValueError(f"Input for {var_name} is invalid.")
            
            value = self.convert_value(value, var_type)
            
            if value is None:
                raise ValueError(f"Converted value for {var_name} is invalid.")
            
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
    
        elif stmt_type == 'void_function': 
            _, function_name, parameters, block = statement
            self.functions[function_name] = {
                'return_type': 'void',
                'parameters': parameters,
                'block': block
            }
            self.debug_print(f"Void function {function_name} defined")

        elif stmt_type == 'call_void_function':  
            function_name = statement[1]
            args = statement[2]
            self.call_void_function(function_name, args)
            return None  
        

    def call_void_function(self, function_name, args):
        """Llama a una función void y ejecuta su bloque de código."""
        if function_name not in self.functions:
            raise NameError(f"Void function '{function_name}' is not defined.")
        
        function_info = self.functions[function_name]
        if function_info['return_type'] != 'void':
            raise TypeError(f"Function '{function_name}' is not a void function.")

        parameters = function_info['parameters']
        block = function_info['block']

        if len(parameters) != len(args):
            raise TypeError(f"Void function '{function_name}' expected {len(parameters)} arguments, but got {len(args)}")

        local_vars = {}
        for param, arg in zip(parameters, args):
            param_type, param_subtype, param_name = param
            arg_value = self.evaluate_expression(arg)

            if param_subtype.lower() != self.get_type_from_value(arg_value).lower():
                arg_value = self.cast_value(arg_value, param_subtype.lower())

            local_vars[param_name] = arg_value

        previous_vars = self.variables.copy()
        self.variables.update(local_vars)

        self.execute_block(block)

        self.variables = previous_vars
        self.debug_print(f"Void function '{function_name}' executed successfully.")
    
    def define_void_function(self, function_name, parameters, block):
        """Guarda una función void en el diccionario de funciones."""
        self.functions[function_name] = {
            'return_type': 'void',
            'parameters': parameters,
            'block': block
        }
        self.debug_print(f"Void function '{function_name}' defined with parameters {parameters}")

    def call_function(self, function_name, args):
        if function_name in self.variables:
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

            if param_subtype.lower() != self.get_type_from_value(arg_value).lower():
                arg_value = self.cast_value(arg_value, param_subtype.lower())

            self.check_type(arg_value, param_subtype.lower())
            local_vars[param_name] = arg_value

        previous_vars = self.variables.copy()
        self.variables.update(local_vars)
        return_value = self.execute_block(block)  
        self.variables = previous_vars  
        if return_value is None:
            raise ValueError(f"Function {function_name} did not return a value.")

        self.check_type(return_value, function_info['return_type'])
        return return_value

    def check_type(self, value, expected_type):
        """Valida que el valor tenga el tipo esperado."""
        if expected_type.lower() != self.get_type_from_value(value).lower():
            raise TypeError(f"Expected {expected_type}, but got {self.get_type_from_value(value)}.")

    def check_type(self, value, expected_type):
        """Valida que el valor tenga el tipo esperado."""
        if expected_type != self.get_type_from_value(value):
            raise TypeError(f"Expected {expected_type}, but got {self.get_type_from_value(value)}.")

    def get_variable_type(self, var_name):
        """Determina el tipo de la variable basada en el nombre."""
        if var_name in self.variables:
            value = self.variables[var_name]
            return self.get_type_from_value(value) 
        return None 

    
    def is_casting_required(self, expected_type, value):
        """ Verifica si el tipo del valor difiere del tipo esperado, lo que requiere un casting """
        type_map = {
            'earth': int,
            'mercury': float,
            'jupiter': float,
            'venus': str,
            'mars': bool,
        }
        return not isinstance(value, type_map.get(expected_type, type(value)))
                
    def cast_value(self, value, target_type):
        """Realiza el cast de un valor a otro tipo explícitamente usando nextPlanet."""

        # De string a int (venus a earth)
        if target_type == 'earth' and isinstance(value, str):  
            if value.isdigit():
                return int(value)
            else:
                raise TypeError(f"Cannot cast string '{value}' to earth (int)")

        # De int a string (earth a venus)
        elif target_type == 'venus' and isinstance(value, int):  
            return str(value)

        # De string a bool (venus a mars)
        elif target_type == 'mars' and isinstance(value, str):  
            if value.lower() == "true" or value == "1":
                return True
            elif value.lower() == "false" or value == "0":
                return False
            else:
                raise TypeError(f"Cannot cast string '{value}' to mars (bool)")

        # De int a bool (earth a mars)
        elif target_type == 'mars' and isinstance(value, int):  
            return value == 1

        # De bool a int (mars a earth)
        elif target_type == 'earth' and isinstance(value, bool):  
            return 1 if value else 0

        # De int o float a float (earth/jupiter a mercury)
        elif target_type == 'mercury' and isinstance(value, (int, float)):  
            return float(value)
        
        # De string a float (venus a mercury)
        elif target_type == 'mercury' and isinstance(value, str):  
            try:
                return float(value)
            except ValueError:
                raise TypeError(f"Cannot cast string '{value}' to mercury (float)")

        # Si el tipo de destino no es soportado o el valor no es del tipo esperado
        raise TypeError(f"Unsupported cast from {type(value).__name__} to {target_type}")

    def get_type_from_value(self, value):
        """ Retorna el tipo basado en el valor """
        if isinstance(value, int):
            return 'earth'
        elif isinstance(value, float):
            return 'mercury'
        elif isinstance(value, str):
            return 'venus'
        elif isinstance(value, bool):
            return 'mars'
        elif value is None: 
            return 'void' 
    
        else:
            raise TypeError(f"Unknown type for value '{value}'")

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
        """Verifica si el valor es del tipo esperado y realiza cast automático entre enteros y booleanos."""
        type_map = {
            'earth': int,
            'mercury': float,
            'jupiter': float,
            'venus': str,
            'mars': bool,
        }
        expected_type = expected_type.lower()
        
        if expected_type == 'mars' and isinstance(value, int):
            value = (value == 1)
        elif expected_type == 'earth' and isinstance(value, bool):
            value = 1 if value else 0

        if expected_type in type_map:
            if not isinstance(value, type_map[expected_type]):
                raise TypeError(f"Expected {type_map[expected_type].__name__}, but got {type(value).__name__}.")
        
        return value

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

    def astro_append(self, list_name, element):
        if list_name not in self.variables:
            raise NameError(f"Astro '{list_name}' is not defined.")
        self.variables[list_name].append(element)
        self.debug_print(f"Element {element} added to astro '{list_name}'")

    def astro_delete_top(self, list_name):
        if list_name not in self.variables:
            raise NameError(f"Astro '{list_name}' is not defined.")
        element = self.variables[list_name].pop()
        self.debug_print(f"Element {element} at top index removed from list '{list_name}'")

    def astro_top(self, list_name):
        if list_name not in self.variables:
            raise NameError(f"Astro '{list_name}' is not defined.")
        if not self.variables[list_name]: 
            raise IndexError(f"Astro '{list_name}' is empty.")
        return self.variables[list_name][-1] 

    def astro_is_vacuum(self, list_name):
        if list_name not in self.variables:
            raise NameError(f"Astro '{list_name}' is not defined.")
        print(len(self.variables[list_name]))
        return (len(self.variables[list_name]) <= 0)
    
    def astro_length(self, list_name):
        if list_name not in self.variables:
            raise NameError(f"Astro '{list_name}' is not defined.")
        return len(self.variables[list_name])

    def nebula_append(self, list_name, element):
        if list_name not in self.variables:
            raise NameError(f"Nebula '{list_name}' is not defined.")
        self.variables[list_name].append(element)
        self.debug_print(f"Element {element} added to astro '{list_name}'")

    def nebula_delete_front(self, list_name):
        if list_name not in self.variables:
            raise NameError(f"Nebula '{list_name}' is not defined.")
        element = self.variables[list_name].pop(0)
        self.debug_print(f"Element {element} at front index removed from list '{list_name}'")

    def nebula_front(self, list_name):
        if list_name not in self.variables:
            raise NameError(f"Nebula '{list_name}' is not defined.")
        if not self.variables[list_name]:  
            raise IndexError(f"Nebula '{list_name}' is empty.")
        return self.variables[list_name][0] 
    
    def nebula_is_vacuum(self, list_name):
        if list_name not in self.variables:
            raise NameError(f"Nebula '{list_name}' is not defined.")
        print(len(self.variables[list_name]))
        return (len(self.variables[list_name]) <= 0)
    
    def nebula_length(self, list_name):
        if list_name not in self.variables:
            raise NameError(f"Nebula '{list_name}' is not defined.")
        return len(self.variables[list_name])
    
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

        if expr_type == 'cast':  
            target_type = expr[1] 
            cast_expr = expr[2]   
            value = self.evaluate_expression(cast_expr)
            return self.cast_value(value, target_type)  

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
        
        elif expr_type == 'astro_isvacuum':
            list_name = expr[1]
            if self.astro_is_vacuum(list_name):
                return "True"
            return "False"
        elif expr_type == 'nebula_isvacuum':
            list_name = expr[1]
            if self.nebula_is_vacuum(list_name):
                return "True"
            return "False"
        elif expr_type == 'nebula_cosmicflow':
            list_name = expr[1]
            return self.nebula_length(list_name)
        elif expr_type == 'astro_count':
            list_name = expr[1]
            return self.astro_length(list_name)
        elif expr_type == 'call_void_function':
            function_name = expr[1]
            args = expr[2]
            self.call_void_function(function_name, args)
            return None 

        elif expr_type == 'call_function':
            function_name = expr[1]
            args = expr[2]
            if function_name in self.variables:  
                vector = self.variables[function_name]
                index = self.evaluate_expression(args[0])
                if not isinstance(index, int) or index < 0 or index >= len(vector):
                    raise IndexError(f"Index {index} out of bounds for vector {function_name}.")
                return vector[index] 
            return self.call_function(function_name, args)

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
            print(f"DEBUG: {message}")
