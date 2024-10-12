import tkinter as tk
from lenguage.lexer import Lexer
from lenguage.parser import Parser
from lenguage.interpretar import Interpretar
import threading
import time

class CodeExecutor:
    def __init__(self, code_input, tokens_display, ast_display, result_display):
        self.code_input = code_input
        self.tokens_display = tokens_display
        self.ast_display = ast_display
        self.result_display = result_display
        self.animating = False

    def execute_code(self):
        source_code = self.code_input.get("1.0", "end-1c")

        # Empezar la animación de compilación
        self.animating = True
        self.result_display.config(state="normal")
        self.result_display.delete("1.0", "end")
        self.result_display.insert("end", "Compilando", "output")
        self.result_display.config(state="disabled")
        
        self.animate_loading()

        # Iniciar la ejecución en un hilo separado
        thread = threading.Thread(target=self.run_interpreter, args=(source_code,))
        thread.start()

    def run_interpreter(self, source_code):
        start_time = time.time()  # Registrar el tiempo de inicio
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

            # Asegurarse de que la animación dure al menos 3 segundos
            elapsed_time = time.time() - start_time
            remaining_time = 3 - elapsed_time
            if remaining_time > 0:
                self.result_display.after(int(remaining_time * 1000), lambda: self.stop_animation_and_show_results(results))
            else:
                self.stop_animation_and_show_results(results)

        except Exception as e:
            elapsed_time = time.time() - start_time
            remaining_time = 3 - elapsed_time
            if remaining_time > 0:
                self.result_display.after(int(remaining_time * 1000), lambda: self.stop_animation_and_show_error(f"Error: {str(e)}"))
            else:
                self.stop_animation_and_show_error(f"Error: {str(e)}")

    def stop_animation_and_show_results(self, results):
        """Detener la animación y mostrar los resultados."""
        self.animating = False
        self.show_results(results)

    def stop_animation_and_show_error(self, error_message):
        """Detener la animación y mostrar el mensaje de error."""
        self.animating = False
        self.display_error(error_message)

    def get_input_from_user(self, prompt):
        """Muestra un cuadro de diálogo personalizado para capturar la entrada del usuario."""
        dialog = tk.Toplevel(self.code_input)
        dialog.title("Input")
        dialog.configure(bg="#1e1e1e")  # Fondo negro
        dialog.geometry("400x150")
        dialog.grab_set()  # Hacer que el diálogo sea modal

        label = tk.Label(dialog, text=prompt, bg="#1e1e1e", fg="#dcdcdc", font=("Consolas", 12))
        label.pack(pady=10)

        entry = tk.Entry(dialog, bg="#2d2d30", fg="#dcdcdc", insertbackground="white", font=("Consolas", 12))
        entry.pack(pady=10)
        entry.focus_set()

        result = {"value": None}

        def on_submit():
            result["value"] = entry.get()
            dialog.destroy()

        submit_button = tk.Button(dialog, text="Aceptar", command=on_submit, bg="#333333", fg="#FFD700", font=("Helvetica", 12))
        submit_button.pack(pady=10)

        dialog.bind("<Return>", lambda event: on_submit())
        dialog.wait_window()  # Esperar a que el cuadro de diálogo se cierre

        return result["value"]

    def animate_loading(self):
        """Animación de texto 'Compilando' con puntos suspensivos."""
        if self.animating:
            current_text = self.result_display.get("1.0", "end-1c")
            if current_text.endswith("..."):
                self.result_display.config(state="normal")
                self.result_display.delete("1.0", "end")
                self.result_display.insert("end", "Compilando", "output")
            else:
                self.result_display.config(state="normal")
                self.result_display.insert("end", ".", "output")
            self.result_display.config(state="disabled")

            # Repetir la animación cada 500ms
            self.result_display.after(500, self.animate_loading)

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
