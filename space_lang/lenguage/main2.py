from lexer import Lexer
from parser import Parser
from interpretar import Interpretar

def input_callback(prompt):
    return input(prompt)

def main():
    source_code1 = """
    planet mars varBoolTrue = true.
    planet mars varBoolFalse = false.
    planet earth var1 = 5.
    planet earth var2 = 5.
    planet mars varBool = false.
    planet earth resultIntSum = var1 + var2. 
    stardock  var1 == var2. 
        star "Resultado de suma de enteros" resultIntSum.
    endStardock.
    supernova.
        star "HOLA" varBool.
    endSupernova.
    """

    lexer = Lexer(source_code1)
    tokens = lexer.tokenize()
    print("=== Tokens ===")
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    ast = parser.parse()
    print("\n=== Arbol estructurado (AST) ===")
    for node in ast:
        print(node)

    interpreter = Interpretar(ast, input_callback)
    print("\n=== Resultado de la Evaluación ===")
    interpreter.evaluate()

if __name__ == '__main__':
    main()
