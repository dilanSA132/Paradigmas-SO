from cx_Freeze import setup, Executable

executables = [Executable("main.py")]

setup(
    name="COSMOSDJ",
    version="1.0",
    description="Lenguage simulator",    
    executables=executables
)
