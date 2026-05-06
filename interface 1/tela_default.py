import tkinter as tk
import tkintermapview
from menu_lateral import Menu_lateral
from mapa import Mapa_tela


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mapa")

    menu = Menu_lateral(root)
    menu.pack(side="left", fill="y")
   
    app = Mapa_tela(root)
    
    root.mainloop() 