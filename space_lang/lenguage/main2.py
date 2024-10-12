from lexer import Lexer
from parser import Parser
from interpretar import Interpretar

def input_callback(prompt):
    return input(prompt)

def main():
    source_code1 = """
    andromeda earth suma[planet earth x, planet earth y]:
        planet earth result = x + y.
        stardust result.
    endAndromeda.

    Stellar myVector = [1, 2, 3, 4, 5, 6].



    planet earth num1 = 10.
    planet earth num2 = 20.

    star "El resultado es" num1.
    """
    source_code2 = """
    planet earth variable = 2.

    perseids variable.
        meteor 1.
            star "valor" variable.
        endMeteor.
        meteor 2.
            star "valor" variable.
        endMeteor.
        commet.
            star "valor" variable.
        endCommet.
    endPerseids.
        
    star "HOLA" variable.
        planet earth num1 = 10.
    planet earth num2 = 20.

    star "El resultado es" num1.
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
