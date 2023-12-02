from tkinter import ttk

class DVDSearchView(ttk.Frame):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.pack()

        label = ttk.Label(self, text="DVDSearchView")
        label.pack()
