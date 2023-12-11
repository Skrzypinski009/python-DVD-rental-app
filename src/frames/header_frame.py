from tkinter import ttk

class HeaderFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        padding_frame = ttk.Frame(self)
        padding_frame.configure(style='Header.TFrame')
        padding_frame.pack(padx=5, pady=5, fill='both')

        self.create_button(padding_frame, 'DVD Search', self.dvd_search_view)
        self.create_button(padding_frame, 'DVD Add', self.dvd_add_view)
        self.create_button(padding_frame, 'Return DVD', self.dvd_return_view)
        self.create_button(padding_frame, 'Rental History', self.history_log_view)
        
    def create_button(self, parent, text, command):
        button_frame = ttk.Frame(parent)
        button_frame.pack(side='left', padx=15)
        button_frame.configure(style='Header.TFrame')
        button = ttk.Button(
            button_frame, 
            text=text, 
            style='Header.TButton',
            width=14,
            command=command
        )
        button.pack()
        return (button, button_frame)
    
    def dvd_search_view(self):
        self.controller.change_view('dvd_search')

    def dvd_add_view(self):
        self.controller.change_view('dvd_add')

    def dvd_return_view(self):
        self.controller.change_view('dvd_return')

    def history_log_view(self):
        self.controller.change_view('history_log')
