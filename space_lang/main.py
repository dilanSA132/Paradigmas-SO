from lexer import Lexer
from parser import Parser
from interpretar import Interpretar

def main():
    source_code = """
    planet earth var1 = 0.
    planet earth var2 = 5.
    
    planet mercury varFloat1 = 4.5.
    planet mercury varFloat2 = 2.5.
    
    planet jupiter varDouble1 = 10.0.
    planet jupiter varDouble2 = 3.0.

    planet venus varString = "Hello, World!".
    
    planet mars varBoolTrue = true.
    planet mars varBoolFalse = false.

    planet earth resultIntSum = var1 + var2.  

    planet mercury resultFloatSum = varFloat1 + varFloat2.
    planet jupiter resultDoubleMul = varDouble1 * varDouble2.

    star "Resultado de suma de enteros" resultIntSum.
    star "Resultado de suma de floats" resultFloatSum.
    star "Resultado de multiplicación de doubles" resultDoubleMul.
    star "Mensaje en cadena" varString.
    star "Valor booleano verdadero" varBoolTrue.
    star "Valor booleano falso" varBoolFalse.

    Stellar myVector = [1, 2, 3, 4, 5].
    star "Impresión del vector" myVector.

    orbit j 0 4.
        star "Elemento del vector" myVector[j].
    endOrbit.

    star "Valor booleano falso" varBoolFalse.
    """
    source_code1 = """
    planet mars varBoolTrue = true.
    planet mars varBoolFalse = false.
    planet earth var1 = 5.
    planet earth var2 = 5.
    planet mars varBool = true.
    planet earth resultIntSum = var1 + var2. 
    stardock varBoolTrue != varBoolFalse and var1 <= var2 or varBool. 
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

    interpreter = Interpretar(ast)
    print("\n=== Resultado de la Evaluación ===")
    interpreter.evaluate()

if __name__ == '__main__':
    main()
