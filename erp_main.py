from tkinter import *
from tkinter import ttk
import subprocess

class App(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)
        self.master = window
        self.init_widgets()
    
    def init_widgets(self):
        frame = Frame(self.master)
        frame.pack(padx=20, pady=20)

        ttk.Label(frame, text="Choose an application", font=("Arial, 12")).grid(row=0, column=0, pady=10)

        buttons = [
            ("Procurement application", self.open_procurement),
            ("Production application", self.open_production),
            ("Sales application", self.open_sales)
        ]

        for idBtn, (text, command) in enumerate(buttons):
            ttk.Button(frame, text=text, command=command, width=30).grid(row=idBtn + 1, column = 0, pady = 5)

    def open_procurement(self):
        subprocess.run(["python", "procurement.py"])

    def open_production(self):
        subprocess.run(["python", "production.py"])

    def open_sales(self):
        subprocess.run(["python", "sales.py"])

root = Tk()
root.title("ERP Software")
root.geometry("400x300")

style = ttk.Style()
style.configure("TButton", font = ("Arial", 10))
style.configure("TLabel", font = ("Arial", 10))

app = App(root)
root.mainloop()