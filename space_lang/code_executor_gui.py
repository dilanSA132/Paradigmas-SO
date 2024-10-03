import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
from lexer import Lexer
from parser import Parser
from interpretar import Interpretar
import re
from structs import Structs

class CodeExecutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Espacial")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1e1e1e")
        self.structs = None
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
        # Añadir color para los planetas
        self.code_input.tag_configure("planet", foreground="#FFD700")  # Color para planetas
        self.code_input.tag_configure("int", foreground="#d69d85")      # Color para enteros
        self.code_input.tag_configure("float", foreground="#4ec9b0")    # Color para flotantes
        self.code_input.tag_configure("double", foreground="#dcdcaa")   # Color para dobles
        self.code_input.tag_configure("string_var", foreground="#ce9178")   # Color para cadenas
        self.code_input.tag_configure("bool", foreground="#569cd6")     # Color para booleanos
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

        self.structs = Structs(self.code_input)

    def create_menu(self):
        menu_bar = Menu(self.root, bg="#333333", fg="#FFD700", activebackground="#212121", activeforeground="#FFD700", relief="flat", font=("Helvetica", 10))
        insert_menu = Menu(menu_bar, tearoff=0, bg="#333333", fg="#FFD700", font=("Helvetica", 10))

        insert_menu.add_command(label="Declaración de enteros", command=self.structs.insert_int_declaration)
        insert_menu.add_command(label="Declaración de flotantes", command=self.structs.insert_float_declaration)
        insert_menu.add_command(label="Declaración de dobles", command=self.structs.insert_double_declaration)
        insert_menu.add_command(label="Declaración de cadena", command=self.structs.insert_string_declaration)
        insert_menu.add_command(label="Declaración de booleanos", command=self.structs.insert_bool_declaration)
        insert_menu.add_command(label="Condicional", command=self.structs.insert_conditional_structure)
        insert_menu.add_command(label="Suma de enteros", command=self.structs.insert_int_sum)
        insert_menu.add_command(label="Suma de flotantes", command=self.structs.insert_float_sum)
        insert_menu.add_command(label="Multiplicación de dobles", command=self.structs.insert_double_mul)
        insert_menu.add_command(label="Bucle", command=self.structs.insert_loop_structure)
        insert_menu.add_command(label="Declaración de vector", command=self.structs.insert_vector_declaration)
        insert_menu.add_command(label="Impresión de vector", command=self.structs.insert_vector_print)

        menu_bar.add_cascade(label="Insertar", menu=insert_menu)
        self.root.config(menu=menu_bar)

    

    def highlight_syntax(self, event=None):
        self.code_input.tag_remove("keyword", "1.0", tk.END)
        self.code_input.tag_remove("number", "1.0", tk.END)
        self.code_input.tag_remove("string", "1.0", tk.END)
        self.code_input.tag_remove("comment", "1.0", tk.END)
        self.code_input.tag_remove("planet", "1.0", tk.END)
        self.code_input.tag_remove("int", "1.0", tk.END)
        self.code_input.tag_remove("float", "1.0", tk.END)
        self.code_input.tag_remove("double", "1.0", tk.END)
        self.code_input.tag_remove("string_var", "1.0", tk.END)
        self.code_input.tag_remove("bool", "1.0", tk.END)

        # Añadir expresión regular para los nombres de los planetas
        planets = r"\b(earth|mars|mercury|venus|jupiter)\b"
        keywords = r"\b(planet|star|orbit|stardock|endStardock|endOrbit|supernova|endSupernova)\b"
        integers = r"\b\d+\b"  # Números enteros
        floats = r"\b\d+\.\d+\b"  # Números flotantes
        doubles = r"\b\d+\.\d+\b"  # Números dobles
        booleans = r"\b(true|false)\b"  # Booleanos
        strings = r'"[^"]*"'
        comments = r'#.*'

        for match in re.finditer(planets, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("planet", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        for match in re.finditer(keywords, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("keyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        for match in re.finditer(integers, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("int", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        for match in re.finditer(floats, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("float", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        for match in re.finditer(doubles, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("double", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        for match in re.finditer(booleans, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("bool", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        for match in re.finditer(strings, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("string_var", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        for match in re.finditer(comments, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("comment", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    def execute_code(self):
        source_code = self.code_input.get("1.0", tk.END)

        try:
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()

            # Muestra tokens en la consola de resultados
            self.show_tokens(tokens)

            parser = Parser(tokens)
            ast = parser.parse()

            # Muestra AST en la consola de resultados
            self.show_ast(ast)

            interpreter = Interpretar(ast)
            results = interpreter.evaluate()

            # Muestra resultados en la consola de resultados
            self.show_results(results)

        except SyntaxError as se:
            self.display_error(f"Error de Sintaxis: {str(se)}")
        except TypeError as te:
            self.display_error(f"Error de Tipo: {str(te)}")
        except IndexError as ie:
            self.display_error(f"Error de Índice: {str(ie)}")
        except ValueError as ve:
            self.display_error(f"Error de Valor: {str(ve)}")
        except Exception as e:
            self.display_error(f"Error desconocido: {str(e)}")

    def show_tokens(self, tokens):
        self.tokens_display.config(state=tk.NORMAL)
        self.tokens_display.delete("1.0", tk.END)
        for token in tokens:
            token_type, token_value = token
            self.tokens_display.insert(tk.END, f"{token}\n", "keyword" if token_type.isupper() else "value")
        self.tokens_display.config(state=tk.DISABLED)

    def show_ast(self, ast):
        self.ast_display.config(state=tk.NORMAL)
        self.ast_display.delete("1.0", tk.END)
        for node in ast:
            self.ast_display.insert(tk.END, f"{node}\n", ("type" if isinstance(node, tuple) else "value"))
        self.ast_display.config(state=tk.DISABLED)

    def show_results(self, results):
        self.result_display.config(state=tk.NORMAL)
        self.result_display.delete("1.0", tk.END)
        if results:
            for result in results:
                self.result_display.insert(tk.END, f"{result}\n", "output")
        else:
            self.result_display.insert(tk.END, "No se ha obtenido un resultado.\n", "output")
        self.result_display.config(state=tk.DISABLED)

    def display_error(self, error_message):
        self.result_display.config(state=tk.NORMAL)
        self.result_display.delete("1.0", tk.END)
        self.result_display.insert(tk.END, f"Error: {error_message}\n", "error")
        self.result_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeExecutorApp(root)
    root.mainloop()
