# tests/test_space_lang.py

import unittest
from space_lang.lexer import Lexer
from space_lang.parser import Parser
from space_lang.interpretar import Interpreter

class TestSpaceLang(unittest.TestCase):

    def test_basic_print(self):
        source_code = "nebula x = 5; star x;"
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(ast)
        interpreter.evaluate()

if __name__ == '__main__':
    unittest.main()
