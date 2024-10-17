from lexer import Lexer
from parser import Parser
from interpretar import Interpretar

def input_callback(prompt):
    return input(prompt)

def main():

    source_code = """
       # Declaración de variables y uso del vector Stellar
    Constellation myVector2 = [0, 20, 23, 4, 51, 6].
    # Crear un vector con valores iniciales
    Stellar myVector = [1, 2, 3, 4, 5].

    # Añadir un nuevo valor al vector
    stellar_add myVector 6.

    star "Vector después de añadir 6" myVector.

    # Remover el valor en la posición 2 del vector
    stellar_remove myVector 2.

    star "Vector después de eliminar el índice 2" myVector.

# Mostrar el tamaño actual del vector
stellar_size myVector.

# Insertar el valor 10 en la posición 1
stellar_place myVector 1 10.

star "Vector después de insertar 10 en la posición 1" myVector.


    # Realizar una operación con el vector dentro de un bucle
    orbit i 0 4 1.
        star "Elemento del vector en la posición" myVector2[i].
    endOrbit.


    

    """
    source_code2 = """
    # Declaración de variables y uso del vector Stellar
    Astro myVector2 = [0, 20, 23, 4, 51, 6].
    astro_launch myVector2 3.
    astro_launch myVector2 36.
    
    astro_orbittop myVector2.
    astro_reentry myVector2.
    planet mars varBoolTrue = astro_isvacuum myVector2.
    # Crear un vector con valores iniciales

    orbit i 0 6 1.
        star "Elemento del vector en la posicion" myVector2[i].
    endOrbit.


    


    

    """

    # Crear el Lexer con el código fuente
    lexer = Lexer(source_code2)
    tokens = lexer.tokenize()

    # Mostrar los tokens generados
    print("=== Tokens ===")
    for token in tokens:
        print(token)

    # Crear el parser con los tokens generados
    parser = Parser(tokens)
    ast = parser.parse()

    # Mostrar el AST (árbol sintáctico abstracto)
    print("\n=== Arbol estructurado (AST) ===")
    for node in ast:
        print(node)

    # Crear el intérprete con el AST
    interpreter = Interpretar(ast, input_callback)

    # Ejecutar la evaluación e interpretar el código
    print("\n=== Resultado de la Evaluación ===")
    interpreter.evaluate()

if __name__ == '__main__':
    main()
