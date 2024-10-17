import tkinter as tk

class Structs:
    
    def __init__(self, code_input):
        self.code_input = code_input

    def insert_loop_structure(self):
        loop_code = "orbit j 0 5 2.\n    star \"Elemento del vector\" myVector[j].\nendOrbit.\n"
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

    def insert_int_sum(self):
        code = "planet earth resultIntSum = var1 + var2.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_float_sum(self):
        code = "planet mercury resultFloatSum = varFloat1 + varFloat2.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_double_mul(self):
        code = "planet jupiter resultDoubleMul = varDouble1 * varDouble2.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_vector_declaration(self):
        code = "Constellation myVector = [0, 20, 23, 4, 51, 6].\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_vector_print(self):
        code = "star \"Impresión del vector\" myVector.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_list_declaration(self):
        code = "Stellar myList = [1, 2, 3, 4, 5, 6].\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_list_print(self):
        code = "star \"Impresión de la lista\" myList.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_Input_print(self):
        code = "starcatch mynum.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_stellar_add(self):
        code = "stellar_add myList 6.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_stellar_remove(self):
        code = "stellar_remove myList 2.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_stellar_size(self):
        code = "stellar_size myList.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_stellar_place(self):
        code = "stellar_place myList 1 10.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_astro_declaration(self):
        code = "Astro stack = [0, 20, 23, 4, 51, 6].\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_astro_push(self):
        code = "astro_launch stack 3.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_astro_pop(self):
        code = "astro_reentry stack.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_astro_top(self):
        code = "astro_orbitTop stack.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_astro_empty(self):
        code = "astro_isVacuum stack.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_astro_size(self):
        code = "astro_count stack.\n"
        self.code_input.insert(tk.INSERT, code)

    def insert_nebula_declaration(self):
        code = "Nebula queue = [1, 12, 23, 44, 51, 67].\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_nebula_enqueue(self):
        code = "nebula_eventHorizon queue 78.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_nebula_dequeue(self):
        code = "nebula_lightSpeed queue.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_nebula_front(self):
        code = "nebula_core queue.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_nebula_empty(self):
        code = "nebula_isVacuum queue.\n"
        self.code_input.insert(tk.INSERT, code)
    def insert_nebula_size(self):
        code = "nebula_cosmicFlow queue.\n"
        self.code_input.insert(tk.INSERT, code)
    
    def insert_switch_structure(self):
        code = "perseids var1.\n  meteor 1.\n    star \"valor X: \" var1.\n  endMeteor.\n  meteor 2.\n    star \"valor Y: \" var1.\n  endMeteor.\n  commet.\n    star \"valor\" var1.\n  endCommet.\nendPerseids.\n"
        self.code_input.insert(tk.INSERT, code)
    def insertFunction(self):
        code = """
        andromeda earth suma[planet earth x, planet earth y]:
            planet earth result = x + y.
            stardust result.
        endAndromeda.

        planet earth num1 = 10.
        planet earth num2 = 2.

        planet earth sumasdf = suma[num1, num2].
        star "El resultado es" sumasdf.
"""
        self.code_input.insert(tk.INSERT, code)
