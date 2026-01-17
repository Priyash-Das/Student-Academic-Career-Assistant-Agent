import tkinter as tk
class BaseWorkspace(tk.Frame):
    def __init__(self, parent, supervisor, colors=None):
        if colors is None:
            colors = {"bg_main": "white"}
        super().__init__(parent, bg=colors["bg_main"])
        self.supervisor = supervisor
        self.colors = colors
    def on_show(self):
        pass
    def on_hide(self):
        pass