from tkinter import ttk

class HeaderFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        padding_frame = ttk.Frame(self)
        padding_frame.configure(style='Header.TFrame')
        padding_frame.pack(padx=5, pady=5, fill='both')

        self.create_button(padding_frame, 'DVD Search')
        self.create_button(padding_frame, 'DVD Add')
        self.create_button(padding_frame, 'Return DVD')
        
    def create_button(self, parent, text):
        button_frame = ttk.Frame(parent)
        button_frame.pack(side='left', padx=5)
        button_frame.configure(style='Header.TFrame')
        button = ttk.Button(
            button_frame, 
            text=text, 
            style='Header.TButton'
        )
        button.pack()
        return (button, button_frame)
        


