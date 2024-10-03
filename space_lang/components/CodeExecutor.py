from lenguage.lexer import Lexer
from lenguage.parser import Parser
from lenguage.interpretar import Interpretar

class CodeExecutor:
    def __init__(self, code_input, tokens_display, ast_display, result_display):
        self.code_input = code_input
        self.tokens_display = tokens_display
        self.ast_display = ast_display
        self.result_display = result_display

    def execute_code(self):
        source_code = self.code_input.get("1.0", "end-1c")

        try:
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            self.show_tokens(tokens)

            parser = Parser(tokens)
            ast = parser.parse()
            self.show_ast(ast)

            interpreter = Interpretar(ast)
            results = interpreter.evaluate()
            self.show_results(results)

        except Exception as e:
            self.display_error(f"Error: {str(e)}")

    def show_tokens(self, tokens):
        self.tokens_display.config(state="normal")
        self.tokens_display.delete("1.0", "end")
        for token in tokens:
            token_type, token_value = token
            self.tokens_display.insert("end", f"{token}\n", "keyword" if token_type.isupper() else "value")
        self.tokens_display.config(state="disabled")

    def show_ast(self, ast):
        self.ast_display.config(state="normal")
        self.ast_display.delete("1.0", "end")
        for node in ast:
            self.ast_display.insert("end", f"{node}\n", "type" if isinstance(node, tuple) else "value")
        self.ast_display.config(state="disabled")

    def show_results(self, results):
        self.result_display.config(state="normal")
        self.result_display.delete("1.0", "end")
        if results:
            for result in results:
                self.result_display.insert("end", f"{result}\n", "output")
        else:
            self.result_display.insert("end", "No se ha obtenido un resultado.\n", "output")
        self.result_display.config(state="disabled")

    def display_error(self, error_message):
        self.result_display.config(state="normal")
        self.result_display.delete("1.0", "end")
        self.result_display.insert("end", error_message, "error")
        self.result_display.config(state="disabled")
