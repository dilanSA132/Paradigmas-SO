import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
from components.Autocomplete import Autocomplete
import re

class CodeExecutorUI:
    def __init__(self, root, execute_callback, structs):
        self.root = root
        self.root.title("Compilador Espacial")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1e1e1e")

        self.structs = structs
        self.execute_callback = execute_callback

        self.keywords = [
            "planet", "star", "starcatch", "orbit", "stardock", "endStardock", 
            "perseids","endPerseids","meteor","endMeteor","commet","endCommet",
            "endOrbit", "supernova", "endSupernova", "earth", "mars", "mercury", 
            "venus", "jupiter", "true", "false", "andromeda", "stardust", "Stellar",
            "endAndromeda", "stardock", "endStardock", "stardust", "stardock",
            "stellar_add", "stellar_remove", "stellar_size", "stellar_place","Constellation",
            "Astro","astro_launch","astro_reentry","astro_orbittop","astro_isvacuum","astro_count",
            "Nebula","nebula_eventHorizon","nebula_lightSpeed","nebula_core","nebula_isVacuum","nebula_cosmicFlow"
        ]

        self.setup_ui()
        self.create_menu()

        self.autocomplete = Autocomplete(self.root, self.code_input, self.keywords)
        self.code_input.bind("<KeyRelease>", self.on_key_release)

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('default')

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
        insert_menu.add_command(label="Impresión del vector", command=self.structs.insert_vector_print)
        insert_menu.add_command(label="Declaración de la lista", command=self.structs.insert_list_declaration)
        insert_menu.add_command(label="Impresión de la lista", command=self.structs.insert_list_print)
        insert_menu.add_command(label="Selector de Variable", command=self.structs.insert_Input_print)
        insert_menu.add_command(label="Switch", command=self.structs.insert_switch_structure)
        insert_menu.add_command(label="Función", command=self.structs.insertFunction)
        insert_menu.add_command(label="Añadir elemento a la lista", command=self.structs.insert_stellar_add)
        insert_menu.add_command(label="Eliminar elemento de la lista", command=self.structs.insert_stellar_remove)   
        insert_menu.add_command(label="Obtener tamaño de la lista", command=self.structs.insert_stellar_size)    
        insert_menu.add_command(label="Insertar en la lista", command=self.structs.insert_stellar_place)

        insert_menu.add_command(label="Declaración de pila", command=self.structs.insert_astro_declaration)
        insert_menu.add_command(label="Método push de pila", command=self.structs.insert_astro_push)
        insert_menu.add_command(label="Método pop de pila", command=self.structs.insert_astro_pop)
        insert_menu.add_command(label="Método top de pila", command=self.structs.insert_astro_top)
        insert_menu.add_command(label="Método es vacio de pila", command=self.structs.insert_astro_empty)
        insert_menu.add_command(label="Obtener tamaño de la pila", command=self.structs.insert_astro_size)

        insert_menu.add_command(label="Declaración de cola", command=self.structs.insert_nebula_declaration)
        insert_menu.add_command(label="Método queue de cola", command=self.structs.insert_nebula_enqueue)
        insert_menu.add_command(label="Método dequeue de cola", command=self.structs.insert_nebula_dequeue)
        insert_menu.add_command(label="Método front de cola", command=self.structs.insert_nebula_front)
        insert_menu.add_command(label="Método es vacio de cola", command=self.structs.insert_nebula_empty)
        insert_menu.add_command(label="Obtener tamaño de la cola", command=self.structs.insert_nebula_size)
        
        menu_bar.add_cascade(label="Insertar", menu=insert_menu)
        self.root.config(menu=menu_bar)

    def on_key_release(self, event):
        """Maneja el autocompletado y el resaltado de sintaxis."""
        self.autocomplete.on_key_release(event)
        self.highlight_syntax()

    def highlight_syntax(self, event=None):
        """Función para resaltar la sintaxis en el editor."""
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

        keywords = r"\b(planet|star|starcatch|orbit|stardock|endStardock|endOrbit|supernova|endSupernova|perseids|endPerseids|meteor|endMeteor|commet|endCommet|andromeda|endAndromeda|stardust|suma|Stellar|stellar_add|stellar_remove|stellar_size|stellar_place|Constellation|Astro|astro_launch|astro_reentry|astro_orbittop|astro_isvacuum|astro_count|Nebula|nebula_eventHorizon|nebula_lightSpeed|nebula_core|nebula_isVacuum|nebula_cosmicFlow)\b"
        integers = r"\b\d+\b"  # Resalta números enteros
        floats = r"\b\d+\.\d+\b"  # Resalta números flotantes
        booleans = r"\b((?i:true)|(?i:false))\b"  # Resalta valores booleanos true/false insensibles a mayúsculas
        strings = r'"[^"]*"'  # Resalta cadenas de texto
        comments = r'#.*'  # Resalta comentarios
        planets = r"\b(earth|mars|mercury|venus|jupiter)\b"  # Resalta tipos de planetas

        # Resaltar palabras clave
        for match in re.finditer(keywords, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("keyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        # Resaltar números enteros
        for match in re.finditer(integers, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("int", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        # Resaltar números flotantes
        for match in re.finditer(floats, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("float", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        # Resaltar booleanos
        for match in re.finditer(booleans, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("bool", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        # Resaltar cadenas de texto
        for match in re.finditer(strings, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("string_var", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        # Resaltar comentarios
        for match in re.finditer(comments, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("comment", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        # Resaltar tipos de planetas (earth, mars, etc.)
        for match in re.finditer(planets, self.code_input.get("1.0", tk.END)):
            self.code_input.tag_add("planet", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
