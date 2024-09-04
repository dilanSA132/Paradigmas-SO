def main():
    source_code = """
    # Declaración de variables de diferentes tipos
    planet earth var1 = 4.
    planet earth var2 = 5.
    
    planet mercury varFloat1 = 4.5.
    planet mercury varFloat2 = 2.5.
    
    planet jupiter varDouble1 = 10.0.
    planet jupiter varDouble2 = 3.0.

    planet venus varString = "Hello, World!".
    
    planet mars varBoolTrue = true.
    planet mars varBoolFalse = false.

    # Sumas, multiplicaciones y otras operaciones
    planet earth resultIntSum = var1 + var2.  # Suma de enteros
    planet mercury resultFloatSum = varFloat1 + varFloat2.  # Suma de floats
    planet jupiter resultDoubleMul = varDouble1 * varDouble2.  # Multiplicación de doubles

    # Prueba con restas
    planet earth resultIntSub = var1 - var2.  # Resta de enteros
    planet mercury resultFloatSub = varFloat1 - varFloat2.  # Resta de floats

    # Prueba con divisiones
    planet jupiter resultDoubleDiv = varDouble1 / varDouble2.  # División de doubles

    # Prueba de errores de tipo
    # planet earth wrongVar = "NotAnInt".  # Error: Asignar string a int
    # planet mercury wrongVar2 = true.  # Error: Asignar booleano a float

    # Impresión de resultados
    star "Resultado de suma de enteros" resultIntSum.
    star "Resultado de resta de enteros" resultIntSub.
    star "Resultado de suma de floats" resultFloatSum.
    star "Resultado de resta de floats" resultFloatSub.
    star "Resultado de multiplicación de doubles" resultDoubleMul.
    star "Resultado de división de doubles" resultDoubleDiv.
    star "Mensaje en cadena" varString.
    star "Valor booleano verdadero" varBoolTrue.
    star "Valor booleano falso" varBoolFalse.
    """

    lexer = Lexer(source_code)
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
