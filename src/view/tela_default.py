import tkinter as tk
import tkintermapview
from view import menu_lateral
from view.paginas import Telas


def start_window_loop():
    root = tk.Tk()
    root.title("Mapa")

    tela = Telas(root)
    
    root.mainloop() 