import tkinter as tk
from structs import Structs
from CodeExecutorUI import CodeExecutorUI
from CodeExecutor import CodeExecutor

def main():
    root = tk.Tk()

    app = None

    def compile_code():
        if app:
            app.code_executor.execute_code()

    structs = Structs(None) 
    app = CodeExecutorUI(root, compile_code, structs)

    app.code_executor = CodeExecutor(app.code_input, app.tokens_display, app.ast_display, app.result_display)

    structs.code_input = app.code_input  

    root.mainloop()

if __name__ == "__main__":
    main()
