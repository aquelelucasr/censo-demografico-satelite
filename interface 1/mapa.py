import tkinter as tk
import tkintermapview
from menu_lateral import Menu_lateral

class Mapa_tela:

    def get_cords(self):
        lat_text = self.set_lat.get()
        lon_text = self.set_long.get()

        try:
            lat = float(lat_text)
            long = float(lon_text)

            self.map_widget.set_position(lat, long)
            self.map_widget.set_zoom(12)
            # map_widget.set_marker(lat, long, text="Nova posição")
        except ValueError:
            print("Por favor, digite apenas números válidos")

    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x800")
        self.root.configure(bg="#B0E0E6")
        

        self.tela()

    
    def tela(self):
        self.frame_lateral = tk.LabelFrame(self.root, width=250, bg="#ADD8E6")
        self.frame_lateral.pack(side="right", fill="both", pady=(20, 15), padx=(0,20))
        self.frame_lateral.pack_propagate(False)

        self.frame_text = tk.Frame(self.frame_lateral, bg="#ADD8E6")
        self.frame_text.pack(expand=True)

        # Entradas de Texto
        tk.Label(self.frame_text, text="Latitude:", bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0,2))
        self.set_lat = tk.Entry(self.frame_text, justify="center")
        self.set_lat.pack(expand=True, pady=(0,5))

        tk.Label(self.frame_text, text="Longitude:", bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0,2))
        self.set_long = tk.Entry(self.frame_text, justify="center")
        self.set_long.pack(expand=True, pady=(0,5))

        # Botão
        self.button_search = tk.Button(self.frame_text, text="Buscar Coordenadas", command=self.get_cords)
        self.button_search.pack()

        # --- Mapa ---
        self.map_label = tk.LabelFrame(self.root, width=250)
        self.map_label.pack(padx=(20,20), pady=(20, 15), side="left", fill="both", expand=True)

        self.map_widget = tkintermapview.TkinterMapView(self.map_label, width=1000, height=800)
        self.map_widget.set_position(-28.9510156, -49.4678388) # Posição inicial (Araranguá)
        self.map_widget.set_zoom(18)
        self.map_widget.pack(fill="both")

   