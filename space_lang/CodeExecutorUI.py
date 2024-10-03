import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
import re

class CodeExecutorUI:
    def __init__(self, root, execute_callback, structs):
        self.root = root
        self.root.title("Compilador Espacial")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1e1e1e")

        self.structs = structs
        self.execute_callback = execute_callback

        self.keywords = ["planet", "star", "orbit", "stardock", "endStardock", "endOrbit", "supernova", 
                         "endSupernova", "earth", "mars", "mercury", "venus", "jupiter", "true", "false"]

        self.setup_ui()
        self.create_menu()
        self.create_autocomplete_popup()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=2)
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)

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
        self.code_input.tag_configure("planet", foreground="#FFD700")  
        self.code_input.tag_configure("int", foreground="#d69d85")     
        self.code_input.tag_configure("float", foreground="#4ec9b0")    
        self.code_input.tag_configure("double", foreground="#dcdcaa")   
        self.code_input.tag_configure("string_var", foreground="#ce9178")  
        self.code_input.tag_configure("bool", foreground="#569cd6")    
        self.code_input.bind("<KeyRelease>", self.on_key_release)

        right_panel = tk.Frame(main_frame, bg="#282828", bd=1, relief=tk.SOLID)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.execute_button = tk.Button(right_panel, text="Compilar", command=self.execute_callback, bg="#333333", fg="#FFD700", font=("Helvetica", 12, "bold"), relief="raised", borderwidth=3, activebackground="#454545", activeforeground="#FFD700")
        self.execute_button.pack(pady=10, padx=5, fill=tk.X)

        tokens_ast_frame = tk.Frame(right_panel, bg="#282828", bd=1, relief=tk.SOLID)
        tokens_ast_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tabs = ttk.Notebook(tokens_ast_frame)
        tabs.pack(fill=tk.BOTH, expand=True)

        tokens_tab = tk.Frame(tabs, bg="#2d2d30")
        tabs.add(tokens_tab, text="Tokens")
        self.tokens_display = scrolledtext.ScrolledText(tokens_tab, wrap=tk.WORD, state=tk.DISABLED, bg="#2d2d30", fg="#dcdcdc", font=("Consolas", 12))
        self.tokens_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tokens_display.tag_configure("keyword", foreground="#569cd6")


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

    def create_autocomplete_popup(self):
        """Crea la ventana emergente de autocompletado."""
        self.popup = tk.Toplevel(self.root)
        self.popup.wm_overrideredirect(True)
        self.popup.geometry("0x0+0+0")
        self.listbox = tk.Listbox(self.popup, bg="#FFFFFF", fg="#000000", selectbackground="#ADD8E6", font=("Consolas", 12))
        self.listbox.pack()
        self.listbox.bind("<Return>", self.select_autocomplete)  # Selección con Enter
        self.listbox.bind("<Double-Button-1>", self.select_autocomplete)  # Selección con doble clic

    def on_key_release(self, event):
        """Esta función maneja tanto el resaltado de sintaxis como el autocompletado."""
        self.highlight_syntax()  
        if event.keysym in ["Up", "Down"]:
            self.listbox.focus_set()
            if event.keysym == "Down":
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(0)
                self.listbox.activate(0)
            elif event.keysym == "Up":
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(tk.END)
                self.listbox.activate(tk.END)
            return

        word = self.get_current_word()
        if word:
            self.show_autocomplete_popup(word)
        else:
            self.hide_autocomplete_popup()

    def get_current_word(self):
        """Obtiene la palabra actual en el cursor."""
        cursor_pos = self.code_input.index(tk.INSERT)
        current_line = self.code_input.get(f"{cursor_pos} linestart", cursor_pos)
        match = re.search(r'\w+$', current_line)
        return match.group(0) if match else None

    def show_autocomplete_popup(self, word):
        """Muestra las sugerencias de autocompletado."""
        matches = [kw for kw in self.keywords if kw.startswith(word)]
        if matches:
            self.listbox.delete(0, tk.END)
            for match in matches:
                self.listbox.insert(tk.END, match)

            if len(matches) > 0:
                x, y, _, _ = self.code_input.bbox(tk.INSERT)
                x += self.code_input.winfo_rootx() + 5
                y += self.code_input.winfo_rooty() + 25

                width = 200 
                height = min(150, 20 * len(matches)) 

                self.popup.geometry(f"{width}x{height}+{x}+{y}")
                self.popup.deiconify()
            else:
                self.hide_autocomplete_popup()
        else:
            self.hide_autocomplete_popup()

    def hide_autocomplete_popup(self):
        """Oculta la ventana emergente de autocompletado."""
        self.popup.withdraw()

    def select_autocomplete(self, event):
        """Selecciona la palabra del listbox y la inserta en el editor."""
        if self.listbox.size() == 0:
            return
        selected = self.listbox.get(tk.ACTIVE)
        cursor_pos = self.code_input.index(tk.INSERT)
        current_line = self.code_input.get(f"{cursor_pos} linestart", cursor_pos)

        new_text = re.sub(r'\w+$', selected, current_line)
        self.code_input.delete(f"{cursor_pos} linestart", cursor_pos)
        self.code_input.insert(f"{cursor_pos} linestart", new_text)

        self.hide_autocomplete_popup()

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

        keywords = r"\b(planet|star|orbit|stardock|endStardock|endOrbit|supernova|endSupernova)\b"
        integers = r"\b\d+\b"  # Números enteros
        floats = r"\b\d+\.\d+\b"  # Números flotantes
        booleans = r"\b(true|false)\b"  # Booleanos
        strings = r'"[^"]*"'
        comments = r'#.*'
        planets = r"\b(earth|mars|mercury|venus|jupiter)\b"  

        for match in re.finditer(keywords, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("keyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(integers, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("int", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(floats, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("float", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(booleans, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("bool", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(strings, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("string_var", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(comments, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("comment", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(planets, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("planet", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

