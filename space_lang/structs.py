import tkinter as tk

class Structs:
    
    def __init__(self, code_input):
        self.code_input = code_input

    def insert_loop_structure(self):
        loop_code = "orbit i 0 10 1.\n    star \"Elemento del bucle\" i.\nendOrbit.\n"
        self.code_input.insert(tk.INSERT, loop_code)

    def insert_conditional_structure(self):
        conditional_code = "stardock var1 < var2.\n    star \"Condición verdadera\" var1.\nendStardock.\n"
        self.code_input.insert(tk.INSERT, conditional_code)

    def insert_variable_declaration(self):
        var_declaration = "planet earth myVar = 10.\n"
        self.code_input.insert(tk.INSERT, var_declaration)

    def insert_int_declaration(self):
        code = "planet earth var1 = 0.\nplanet earth var2 = 5.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_float_declaration(self):
        code = "planet mercury varFloat1 = 4.5.\nplanet mercury varFloat2 = 2.5.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_double_declaration(self):
        code = "planet jupiter varDouble1 = 10.0.\nplanet jupiter varDouble2 = 3.0.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_string_declaration(self):
        code = 'planet venus varString = "Hello, World!".\n'
        self.code_input.insert(tk.INSERT, code)

    def insert_bool_declaration(self):
        code = "planet mars varBoolTrue = true.\nplanet mars varBoolFalse = false.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_conditional_structure(self):
        conditional_code = "stardock var1 < var2.\n    star planet earth myVar = 10.\nendStardock.\n"
        self.code_input.insert(tk.INSERT, conditional_code)

    def insert_int_sum(self):
        code = "planet earth resultIntSum = var1 + var2.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_float_sum(self):
        code = "planet mercury resultFloatSum = varFloat1 + varFloat2.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_double_mul(self):
        code = "planet jupiter resultDoubleMul = varDouble1 * varDouble2.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_loop_structure(self):
        loop_code = "orbit j 0 5 2.\n    star \"Elemento del vector\" myVector[j].\nendOrbit.\n"
        self.code_input.insert(tk.INSERT, loop_code)

    def insert_vector_declaration(self):
        code = "Stellar myVector = [1, 2, 3, 4, 5, 6].\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_vector_print(self):
        code = "star \"Impresión del vector\" myVector.\n"
        self.code_input.insert(tk.INSERT, code)
