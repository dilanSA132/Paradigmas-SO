import tkinter as tk

class Structs:
    
    def __init__(self, code_input):
        self.code_input = code_input

    def insert_loop_structure(self):
        loop_code = "orbit j 0 5 2.\n    star \"Elemento del vector\" myVector[j].\nendOrbit.\n"
        self.code_input.insert(tk.INSERT, loop_code)

    def insert_conditional_structure(self):
        conditional_code = "stardock var1 < var2.\n    star \"Menor \" var1.\nendStardock.\nsupernova.\n  star \"Menor \" var2.\nendSupernova.\n"
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
        
    def insert_constellation_and_loop(self):
        code = """Constellation myVector = [0, 20, 23, 4, 51, 6].

    moon display_info [planet venus message]:
        orbit j 0 5 2.
            star "Elemento del vector" myVector[j].
        endOrbit.
        star message.
    endMoon
    """
        self.code_input.insert(tk.INSERT, code)

    def insert_moon_function(self):
        code = """moon display_info [planet venus message]:
        star message.
    endMoon
    """
        self.code_input.insert(tk.INSERT, code)

    def insert_int_function(self):
        code = """andromeda earth suma[planet earth x, planet earth y]:
        planet earth result = x + y.
        stardust result.
    endAndromeda
    """
        self.code_input.insert(tk.INSERT, code)

    def insert_string_function(self):
        code = """andromeda venus suma[planet venus x, planet venus y]:
        planet venus result = x + y.
        stardust result.
    endAndromeda
    """
        self.code_input.insert(tk.INSERT, code)

    def insert_bool_function(self):
        code = """andromeda mars suma[planet mars x, planet venus y]:
        planet mars result = 1.
        stardust result.
    endAndromeda
    """
        self.code_input.insert(tk.INSERT, code)

    def insert_float_function(self):
        code = """andromeda mercury suma[planet mercury x]:
        stardust x + 1.45.
    endAndromeda
    """
        self.code_input.insert(tk.INSERT, code)

    def insert_double_function(self):
        code = """andromeda jupiter suma[planet jupiter x]:
        stardust x + 1.45.
    endAndromeda
    """
        self.code_input.insert(tk.INSERT, code)

    def insert_casting_example(self):
        code = """planet earth intVar = nextPlanet["1"].  # Casteo explícito de string a int
        planet venus strVar = nextPlanet[intVar].  # Casteo explícito de int a string
        planet mars boolVar = nextPlanet[strVar].  # Casteo explícito de string a booleano
        star "Valor casteado" boolVar.
    """
        self.code_input.insert(tk.INSERT, code)
    
    def insertCalculator(self):
        code = """andromeda mercury add[planet mercury a,planet mercury b]:
    planet mercury result = a + b.
    stardust result.
endAndromeda

andromeda mercury subtract[planet mercury a,planet mercury b]:
    planet mercury result = a - b.
    stardust result.
endAndromeda

andromeda mercury multiply[planet mercury a,planet mercury b]:
    planet mercury result = a * b.
    stardust result.
endAndromeda

andromeda mercury divide[planet mercury a, planet mercury b]:
    stardock b == 0.
        star "Can´t divide by zero".
    planet mercury result = 0.0.
        endStardock.
        supernova.
        planet mercury result = a / b.
    endSupernova. 
    stardust result.
endAndromeda

moon print_result[planet mercury result]:
    star "Result is: " result.
endMoon

moon calculator[planet mercury x, planet mercury y, planet venus operation]:

    perseids operation.
        meteor "+".
            planet mercury result = add[x, y].
        endMeteor.
        meteor "-".
            planet mercury result = subtract[x, y].
        endMeteor.
        meteor "*".
            planet mercury result = multiply[x, y].
        endMeteor.
        meteor "/".
            planet mercury result = divide[x, y].
        endMeteor.
        commet.
            star "Invalid operation.".
        planet mercury result = 0.0.
        endCommet.
    endPerseids.

    sun print_result[result].
endMoon


star "--- Calculadora ---".
    planet mercury x = 0.0.
    planet mercury y = 0.0.
    
    planet venus operation = "+".

    starcatch "Enter first number: " x.
    starcatch "Enter second number: " y. 

    starcatch "Choose operation + - / * " operation.

sun calculator[x,y,operation].
"""
        self.code_input.insert(tk.INSERT, code)

    def insertSort(self):
        code = """
Stellar list = [6, 8, 2, 4, 1, 5, 6, 5, 3, 245, 6, 743, 5, 4, 6, 1346, 6, 1, 2, 987, 453, 32, 91, 21, 73, 67, 19, 38, 555, 320, 89, 12, 47, 63, 101, 333, 404, 159, 26, 88, 420, 17, 34, 66, 312, 234, 567, 789, 654, 876, 123, 345, 2345, 876, 543, 21, 432, 765, 567, 89, 987, 201, 345, 675, 189, 320, 457, 612, 104, 98, 73, 54, 33, 29, 16, 11, 95, 64, 88, 72, 13, 97, 91, 22, 27, 78, 36, 59, 44, 83, 17, 5, 42, 31, 60, 92, 71, 90, 69, 58, 41].

moon sort[]:
planet earth length = stellar_size list.
star "" length.
   orbit j length-1 0 1.
    	orbit i 0 length-2 1.
	  star list.
	  planet earth index = i+1.
	  stardock list[i] > list[index].
    		planet earth var = list[i].
		stellar_remove list i.
		stellar_place list i list[i].
		stellar_remove list index.
		stellar_place list index var.
	   endStardock.
	endOrbit.
   endOrbit.
star list.
endMoon
    
sun sort[].
"""
        self.code_input.insert(tk.INSERT, code)