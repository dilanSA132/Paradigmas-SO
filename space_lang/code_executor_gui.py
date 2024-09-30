import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
from lexer import Lexer
from parser import Parser
from interpretar import Interpretar
import re

class CodeExecutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Espacial")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1e1e1e")

        self.setup_ui()
        self.create_menu()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar la cuadrícula principal
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=2)
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)

        # Editor de código (arriba a la izquierda)
        code_frame = tk.Frame(main_frame, bg="#282828", bd=1, relief=tk.SOLID)
        code_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        editor_label = tk.Label(code_frame, text="Editor de Código", bg="#282828", fg="#FFD700", font=("Helvetica", 10, "bold"))
        editor_label.pack(anchor="w", padx=5)

        self.code_input = scrolledtext.ScrolledText(code_frame, wrap=tk.WORD, bg="#2d2d30", fg="#dcdcdc", insertbackground="white", font=("Consolas", 12))
        self.code_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.code_input.tag_configure("keyword", foreground="#569cd6")
        self.code_input.tag_configure("number", foreground="#b5cea8")
        self.code_input.tag_configure("string", foreground="#ce9178")
        self.code_input.tag_configure("comment", foreground="#6a9955")
        self.code_input.bind("<KeyRelease>", self.highlight_syntax)

        # Panel derecho que incluye el botón de compilar y los tokens y AST
        right_panel = tk.Frame(main_frame, bg="#282828", bd=1, relief=tk.SOLID)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.execute_button = tk.Button(right_panel, text="Compilar", command=self.execute_code, bg="#333333", fg="#FFD700", font=("Helvetica", 12, "bold"), relief="raised", borderwidth=3, activebackground="#454545", activeforeground="#FFD700")
        self.execute_button.pack(pady=10, padx=5, fill=tk.X)
        
        self.execute_button.config(cursor="hand2")

        # Tokens y AST frame
        tokens_ast_frame = tk.Frame(right_panel, bg="#282828", bd=1, relief=tk.SOLID)
        tokens_ast_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tabs = ttk.Notebook(tokens_ast_frame)
        tabs.pack(fill=tk.BOTH, expand=True)

        # Tab para Tokens
        tokens_tab = tk.Frame(tabs, bg="#2d2d30")
        tabs.add(tokens_tab, text="Tokens")
        self.tokens_display = scrolledtext.ScrolledText(tokens_tab, wrap=tk.WORD, state=tk.DISABLED, bg="#2d2d30", fg="#dcdcdc", font=("Consolas", 12))
        self.tokens_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tokens_display.tag_configure("keyword", foreground="#569cd6")
        self.tokens_display.tag_configure("number", foreground="#b5cea8")
        self.tokens_display.tag_configure("string", foreground="#ce9178")

        # Tab para AST
        ast_tab = tk.Frame(tabs, bg="#2d2d30")
        tabs.add(ast_tab, text="Árbol Sintáctico")
        self.ast_display = scrolledtext.ScrolledText(ast_tab, wrap=tk.WORD, state=tk.DISABLED, bg="#2d2d30", fg="#dcdcdc", font=("Consolas", 12))
        self.ast_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.ast_display.tag_configure("type", foreground="#4ec9b0")
        self.ast_display.tag_configure("value", foreground="#dcdcaa")

        result_frame = tk.Frame(main_frame, bg="#282828", bd=1, relief=tk.SOLID)
        result_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        result_label = tk.Label(result_frame, text="Consola de Resultados", bg="#282828", fg="#FFD700", font=("Helvetica", 10, "bold"))
        result_label.pack(anchor="w", padx=5)

        self.result_display = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#2d2d30", fg="#dcdcdc", font=("Consolas", 12))
        self.result_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_display.tag_configure("output", foreground="#b5cea8")
        self.result_display.tag_configure("error", foreground="#ff5555")

    def create_menu(self):
        menu_bar = Menu(self.root, bg="#333333", fg="#FFD700", activebackground="#212121", activeforeground="#FFD700", relief="flat", font=("Helvetica", 10))
        insert_menu = Menu(menu_bar, tearoff=0, bg="#333333", fg="#FFD700", font=("Helvetica", 10))

        insert_menu.add_command(label="Bucle", command=self.insert_loop_structure)
        insert_menu.add_command(label="Condicional", command=self.insert_conditional_structure)
        insert_menu.add_command(label="Declaración de variable", command=self.insert_variable_declaration)

        menu_bar.add_cascade(label="Insertar", menu=insert_menu)
        self.root.config(menu=menu_bar)

    def insert_loop_structure(self):
        loop_code = "orbit i 0 10 1.\n    star \"Elemento del bucle\" i.\nendOrbit.\n"
        self.code_input.insert(tk.INSERT, loop_code)

    def insert_conditional_structure(self):
        conditional_code = "stardock var1 < var2.\n    star \"Condición verdadera\" var1.\nendStardock.\n"
        self.code_input.insert(tk.INSERT, conditional_code)

    def insert_variable_declaration(self):
        var_declaration = "planet earth myVar = 10.\n"
        self.code_input.insert(tk.INSERT, var_declaration)

    def highlight_syntax(self, event=None):
        self.code_input.tag_remove("keyword", "1.0", tk.END)
        self.code_input.tag_remove("number", "1.0", tk.END)
        self.code_input.tag_remove("string", "1.0", tk.END)
        self.code_input.tag_remove("comment", "1.0", tk.END)

        keywords = r"\b(planet|star|orbit|stardock|endStardock|endOrbit|supernova|endSupernova)\b"
        numbers = r"\b\d+\b"
        strings = r'"[^"]*"'
        comments = r'#.*'

        for match in re.finditer(keywords, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("keyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        for match in re.finditer(numbers, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("number", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        for match in re.finditer(strings, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("string", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        for match in re.finditer(comments, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("comment", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    def execute_code(self):
        source_code = self.code_input.get("1.0", tk.END)

        try:
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            interpreter = Interpretar(ast)
            results = interpreter.evaluate()

            self.ast_display.config(state=tk.NORMAL)
            self.ast_display.delete("1.0", tk.END)
            for node in ast:
                self.ast_display.insert(tk.END, f"{node}\n", ("type" if isinstance(node, tuple) else "value"))
            self.ast_display.config(state=tk.DISABLED)

            self.tokens_display.config(state=tk.NORMAL)
            self.tokens_display.delete("1.0", tk.END)
            for token in tokens:
                token_type, token_value = token
                self.tokens_display.insert(tk.END, f"{token}\n", "keyword" if token_type.isupper() else "value")
            self.tokens_display.config(state=tk.DISABLED)

            self.result_display.config(state=tk.NORMAL)
            self.result_display.delete("1.0", tk.END)
            if results:
                for result in results:
                    self.result_display.insert(tk.END, f"{result}\n", "output")
            else:
                self.result_display.insert(tk.END, "No se ha obtenido un resultado.\n", "output")
            self.result_display.config(state=tk.DISABLED)

        except Exception as e:
            self.result_display.config(state=tk.NORMAL)
            self.result_display.delete("1.0", tk.END)
            self.result_display.insert(tk.END, f"Error: {e}", "error")
            self.result_display.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    app = CodeExecutorApp(root)
    root.mainloop()
