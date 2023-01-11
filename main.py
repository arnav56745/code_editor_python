import tkinter as tk
from tkinter import ttk, BOTH, filedialog, messagebox
from tkterm import Terminal
from chlorophyll import CodeView
import pygments.lexer, os

root = tk.Tk()


###
###
root.title("Code Editor - Untitled.py")
###
nbook = ttk.Notebook(root)
frame = ttk.Frame(nbook)
nbook.add(frame, text="Untitled.py")
nbook.pack(fill="both", expand=True)
file_path: str = ""


def set_file_path(a):
    global file_path
    file_path = a


###
t = CodeView(
    root,
    lexer=pygments.lexers.PythonLexer,
    color_scheme="monokai",
    font=("JetBrains Mono", 13, "normal"),
)
t.pack(fill="both", expand=True)
terminal = Terminal(root, width=200, height=200)
trun = terminal.run_command
trun("echo Built with tkterm, chlorophyll and pygments")


def save_as():
    global file
    if file_path == "":
        file = filedialog.asksaveasfilename(
            filetypes=[
                (
                    "Python Files",
                    "*.py",
                )
            ]
        )
    else:
        file = file_path
    with open(file, "w") as f:
        code = t.get("1.0", tk.END)
        f.write(code)
        nbook.add(frame, text=os.path.basename(file))
        set_file_path(file)


def save():
    pass


def run_code():
    try:
        trun(f'python "{file}"')
    except NameError:
        res = messagebox.askquestion(
            "Save file?", "Do you want to save the file before running the code?"
        )
        if res == "yes":
            save_as()


def open_file():
    _file = filedialog.askopenfilename(
        filetypes=[
            (
                "Python Files",
                "*.py",
            )
        ]
    )
    with open(_file, "r") as _f:
        _t = _f.read()
        t.delete("1.0", tk.END)
        t.insert("1.0", _t)
        root.title(f"Code Editor - {_file}")
        nbook.add(frame, text=os.path.basename(_file))
        set_file_path(_file)


terminal.pack(fill=BOTH, expand=True)
root.minsize(root.winfo_width(), root.winfo_height())
menu = tk.Menu(root)
file_menu = tk.Menu(menu)
run_menu = tk.Menu(menu)
term_menu = tk.Menu(menu)
file_menu.add_command(label="Open file...", command=open_file)
file_menu.add_command(label="Save file...", command=save_as)

file_menu.add_command(label="Save file as...", command=save_as)
file_menu.add_command(label="Exit", command=root.destroy)
run_menu.add_command(label="Run code...", command=run_code)

term_menu.add_command(label="Clear Terminal", command=terminal.clear_screen)
menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Run", menu=run_menu)
menu.add_cascade(label="Terminal", menu=term_menu)
root.config(menu=menu)
root.mainloop()
