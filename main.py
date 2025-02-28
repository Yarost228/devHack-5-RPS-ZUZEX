from tkinter import *
from tkinter import ttk
from random import *

class App(ttk.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

if __name__ == '__main__':
    root = Tk()
    root.title('RPS-ZUZEX')
    root.update()
    root.geometry('600x400')
    root["bg"] = "#383838"
    labelText = Label(root, text='КАМЕНЬ-НОЖНИЦЫ-БУМАГА', fg='white', font=('Comic Sans MS', 20), bg='black')
    playButton = Button(root, )
    root.update()
    labelText.place(relx=-0.4, rely=0.2, anchor='center')
    mainloop()
