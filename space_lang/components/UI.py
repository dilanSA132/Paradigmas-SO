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
            "Nebula","nebula_eventHorizon","nebula_lightSpeed","nebula_core","nebula_isVacuum","nebula_cosmicFlow","sun","moon", "endMoon" ,"and", "nextPlanet"       
        ]

        self.setup_ui()
        self.create_menu()

        self.autocomplete = Autocomplete(self.root, self.code_input, self.keywords)
        self.code_input.bind("<KeyRelease>", self.on_key_release)
        self.code_input.bind("<KeyRelease-Return>", self.update_line_numbers) 

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

        self.line_numbers = tk.Text(code_frame, width=4, bg="#2d2d30", fg="#dcdcdc", state=tk.DISABLED, font=("Consolas", 12))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.code_input = scrolledtext.ScrolledText(code_frame, wrap=tk.WORD, bg="#2d2d30", fg="#dcdcdc", insertbackground="white", font=("Consolas", 12))
        self.code_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        self.code_input.config(yscrollcommand=self.sync_scroll)
        self.line_numbers.config(yscrollcommand=self.sync_scroll)

        # Agregar binding para el scroll del ratón
        self.code_input.bind("<MouseWheel>", self.on_mouse_wheel)
        self.line_numbers.bind("<MouseWheel>", self.on_mouse_wheel)
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
        self.update_line_numbers()
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

        # Crear el menú principal "Insertar"
        insert_menu = Menu(menu_bar, tearoff=0, bg="#333333", fg="#FFD700", font=("Helvetica", 10))

        # Submenú de Declaraciones
        declarations_menu = Menu(insert_menu, tearoff=0, bg="#333333", fg="#FFD700", font=("Helvetica", 10))
        declarations_menu.add_command(label="Declaración de enteros", command=self.structs.insert_int_declaration)
        declarations_menu.add_command(label="Declaración de flotantes", command=self.structs.insert_float_declaration)
        declarations_menu.add_command(label="Declaración de dobles", command=self.structs.insert_double_declaration)
        declarations_menu.add_command(label="Declaración de cadena", command=self.structs.insert_string_declaration)
        declarations_menu.add_command(label="Declaración de booleanos", command=self.structs.insert_bool_declaration)
        declarations_menu.add_command(label="Declaración de vector", command=self.structs.insert_vector_declaration)
        declarations_menu.add_command(label="Declaración de lista", command=self.structs.insert_list_declaration)
        declarations_menu.add_command(label="Declaración de pila", command=self.structs.insert_astro_declaration)
        declarations_menu.add_command(label="Declaración de cola", command=self.structs.insert_nebula_declaration)

        # Submenú de Estructuras
        structures_menu = Menu(insert_menu, tearoff=0, bg="#333333", fg="#FFD700", font=("Helvetica", 10))
        structures_menu.add_command(label="Bucle", command=self.structs.insert_loop_structure)
        structures_menu.add_command(label="Condicional", command=self.structs.insert_conditional_structure)
        structures_menu.add_command(label="Switch", command=self.structs.insert_switch_structure)
        structures_menu.add_command(label="Impresión del vector", command=self.structs.insert_vector_print)
        structures_menu.add_command(label="Impresión de la lista", command=self.structs.insert_list_print)
        structures_menu.add_command(label="Añadir elemento a la lista", command=self.structs.insert_stellar_add)
        structures_menu.add_command(label="Eliminar elemento de la lista", command=self.structs.insert_stellar_remove)
        structures_menu.add_command(label="Obtener tamaño de la lista", command=self.structs.insert_stellar_size)
        structures_menu.add_command(label="Insertar en la lista", command=self.structs.insert_stellar_place)
        structures_menu.add_command(label="Método push de pila", command=self.structs.insert_astro_push)
        structures_menu.add_command(label="Método pop de pila", command=self.structs.insert_astro_pop)
        structures_menu.add_command(label="Método top de pila", command=self.structs.insert_astro_top)
        structures_menu.add_command(label="Método es vacío de pila", command=self.structs.insert_astro_empty)
        structures_menu.add_command(label="Obtener tamaño de la pila", command=self.structs.insert_astro_size)
        structures_menu.add_command(label="Método enqueue de cola", command=self.structs.insert_nebula_enqueue)
        structures_menu.add_command(label="Método dequeue de cola", command=self.structs.insert_nebula_dequeue)
        structures_menu.add_command(label="Método front de cola", command=self.structs.insert_nebula_front)
        structures_menu.add_command(label="Método es vacío de cola", command=self.structs.insert_nebula_empty)
        structures_menu.add_command(label="Obtener tamaño de la cola", command=self.structs.insert_nebula_size)

        # Submenú de Funciones
        functions_menu = Menu(insert_menu, tearoff=0, bg="#333333", fg="#FFD700", font=("Helvetica", 10))
        functions_menu.add_command(label="Función moon (void)", command=self.structs.insert_moon_function)
        functions_menu.add_command(label="Función suma de enteros", command=self.structs.insert_int_function)
        functions_menu.add_command(label="Función suma de cadenas", command=self.structs.insert_string_function)
        functions_menu.add_command(label="Función suma de booleanos", command=self.structs.insert_bool_function)
        functions_menu.add_command(label="Función suma de flotantes", command=self.structs.insert_float_function)
        functions_menu.add_command(label="Función suma de dobles", command=self.structs.insert_double_function)

        # Submenú de Casting
        casting_menu = Menu(insert_menu, tearoff=0, bg="#333333", fg="#FFD700", font=("Helvetica", 10))
        casting_menu.add_command(label="Casteos", command=self.structs.insert_casting_example)

        # Submenú de Ejemplos
        examples_menu = Menu(insert_menu, tearoff=0, bg="#333333", fg="#FFD700", font=("Helvetica", 10))
        examples_menu.add_command(label="Calculadora", command=self.structs.insertCalculator)
        examples_menu.add_command(label="Ordenamiento", command=self.structs.insertSort)
        # Agregar los submenús al menú "Insertar"
        insert_menu.add_cascade(label="Declaraciones", menu=declarations_menu)
        insert_menu.add_cascade(label="Estructuras", menu=structures_menu)
        insert_menu.add_cascade(label="Funciones", menu=functions_menu)
        insert_menu.add_cascade(label="Casting", menu=casting_menu)
        insert_menu.add_cascade(label="Ejemplos", menu=examples_menu)

        # Agregar el menú "Insertar" al menú principal
        menu_bar.add_cascade(label="Insertar", menu=insert_menu)

        # Configurar la barra de menú en la raíz de la ventana
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

        keywords = r"\b(planet|star|sun|moon|nextPlanet|endMoon|starcatch|orbit|stardock|endStardock|endOrbit|supernova|endSupernova|perseids|endPerseids|meteor|endMeteor|commet|endCommet|andromeda|endAndromeda|stardust|suma|Stellar|stellar_add|stellar_remove|stellar_size|stellar_place|Constellation|Astro|astro_launch|astro_reentry|astro_orbitTop|astro_isVacuum|astro_count|Nebula|nebula_eventHorizon|nebula_lightSpeed|nebula_core|nebula_isVacuum|nebula_cosmicFlow)\b"
        integers = r"\b\d+\b" 
        floats = r"\b\d+\.\d+\b" 
        booleans = r"\b((?i:true)|(?i:false))\b"  
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

    def update_line_numbers(self, event=None):
        """Actualizar el widget de números de línea en cada cambio de texto."""
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)

        line_count = self.code_input.index(tk.END).split('.')[0]
        line_numbers_string = "\n".join(str(i) for i in range(1, int(line_count)))
        
        self.line_numbers.insert(tk.INSERT, line_numbers_string)
        self.line_numbers.config(state=tk.DISABLED)

    def sync_scroll(self, *args):
        """Sincroniza el scroll entre el editor de código y los números de línea."""
        self.line_numbers.yview_moveto(args[0])
        self.code_input.yview_moveto(args[0])

    def on_mouse_wheel(self, event):
        """Permite el scroll usando la rueda del ratón y lo sincroniza."""
        self.code_input.yview_scroll(int(-1*(event.delta/120)), "units")
        self.line_numbers.yview_scroll(int(-1*(event.delta/120)), "units")
