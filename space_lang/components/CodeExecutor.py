import tkinter as tk
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

            # Pasar la función de entrada al intérprete
            interpreter = Interpretar(ast, self.get_input_from_user)
            results = interpreter.evaluate()
            self.show_results(results)

        except Exception as e:
            self.display_error(f"Error: {str(e)}")
            
    def get_input_from_user(self, prompt):
        """Muestra un cuadro de diálogo personalizado para capturar la entrada del usuario."""
        dialog = tk.Toplevel(self.code_input)
        dialog.title("Input")
        dialog.configure(bg="#1e1e1e")  # Fondo negro
        dialog.geometry("400x150")
        dialog.grab_set()  # Hacer que el diálogo sea modal

        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        label = tk.Label(dialog, text=prompt, bg="#1e1e1e", fg="#dcdcdc", font=("Consolas", 12))
        label.pack(pady=10, anchor="center")  

        entry = tk.Entry(dialog, bg="#2d2d30", fg="#dcdcdc", insertbackground="white", font=("Consolas", 12))
        entry.pack(pady=10, anchor="center") 
        entry.focus_set()

        result = {"value": None}

        def on_submit():
            result["value"] = entry.get()
            dialog.destroy()

        submit_button = tk.Button(dialog, text="Aceptar", command=on_submit, bg="#333333", fg="#FFD700", font=("Helvetica", 12))
        submit_button.pack(pady=10, anchor="center")  # Centrar el botón

        dialog.bind("<Return>", lambda event: on_submit())
        dialog.wait_window()  

        return result["value"]


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
            self.display_result_line(results, 0)  # Comienza con el primer resultado
        else:
            self.result_display.insert("end", "No se ha obtenido un resultado.\n", "output")
        
        self.result_display.config(state="disabled")

    def display_result_line(self, results, index):
        """Función auxiliar para mostrar cada línea de resultado progresivamente."""
        if index < len(results):
            self.result_display.config(state="normal")  
            self.result_display.insert("end", f"{results[index]}\n", "output")
            self.result_display.see("end")  
            self.result_display.config(state="disabled")  
            self.result_display.after(1000, lambda: self.display_result_line(results, index + 1))
    
    def display_error(self, error_message):
        self.result_display.config(state="normal")
        self.result_display.delete("1.0", "end")
        self.result_display.insert("end", error_message, "error")
        self.result_display.config(state="disabled")
