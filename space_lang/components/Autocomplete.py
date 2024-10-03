import tkinter as tk
import re

class Autocomplete:
    def __init__(self, root, code_input, keywords):
        self.root = root
        self.code_input = code_input
        self.keywords = keywords
        self.create_autocomplete_popup()

    def create_autocomplete_popup(self):
        """Crea la ventana emergente de autocompletado."""
        self.popup = tk.Toplevel(self.root)
        self.popup.wm_overrideredirect(True)
        self.popup.geometry("0x0+0+0")
        self.listbox = tk.Listbox(self.popup, bg="#FFFFFF", fg="#000000", selectbackground="#ADD8E6", font=("Consolas", 12))
        self.listbox.pack()
        self.listbox.bind("<Return>", self.select_autocomplete)  
        self.listbox.bind("<Double-Button-1>", self.select_autocomplete)  

    def on_key_release(self, event):
        """Esta función maneja tanto el resaltado de sintaxis como el autocompletado."""
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
        self.popup.withdraw()

    def select_autocomplete(self, event):
        if self.listbox.size() == 0:
            return
        selected = self.listbox.get(tk.ACTIVE)
        cursor_pos = self.code_input.index(tk.INSERT)
        current_line = self.code_input.get(f"{cursor_pos} linestart", cursor_pos)

        new_text = re.sub(r'\w+$', selected, current_line)
        self.code_input.delete(f"{cursor_pos} linestart", cursor_pos)
        self.code_input.insert(f"{cursor_pos} linestart", new_text)

        self.hide_autocomplete_popup()
