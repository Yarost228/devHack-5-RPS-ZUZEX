from tkinter import *
from tkinter import ttk
from random import *

class App(ttk.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

if __name__ == '__main__':
    root = Tk()
    root.geometry('600x400')
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    mainloop()
