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

    planet earth num1 = 10.
    planet earth num2 = 20.
    planet earth resultado = suma[num1, num2].
    star "El resultado es" resultado.
    """

    # Crear el Lexer con el código fuente
    lexer = Lexer(source_code1)
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
