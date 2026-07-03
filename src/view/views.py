import tkinter as tk
import tkintermapview

from tkinter import ttk, Scrollbar
from src.controller.C_shared import get_center
from src.controller.Functions import debug_print, get_map_image
from pathlib import Path
from PIL import Image, ImageTk
from src.model.databaseModel import get_search_by_term,get_all_history,get_result_by_id


class DetailView(tk.Toplevel):
    """A secondary window that accepts arguments."""

    def __init__(self, parent, slug):
        super().__init__(parent)
        self.title("Detail View")
        self.geometry("833x558")
        self.configure(bg="#B0E0E6")
        self.data = {"ID":-1,"SLUG":"","TL_LAT":0.0, "TL_LON":0.0, "BR_LAT":0.0, "BR_LON":0.0, "CENT":0.0}


        self.frame_lateral = tk.LabelFrame(self, width=250, bg="#ADD8E6")
        self.frame_lateral.pack(side="right", fill="y", pady=(20, 15), padx=(0, 20))
        self.frame_lateral.pack_propagate(False)

        self.frame_text = tk.Frame(self.frame_lateral, bg="#ADD8E6",)
        self.frame_text.pack(expand=True)
        search_data = get_search_by_term(slug)

        self.data["ID"],self.data["SLUG"],self.data["TL_LAT"],self.data["TL_LON"],self.data["BR_LAT"],self.data["BR_LON"] = search_data[0]

        center_lat,center_lon  = get_center(self.data["TL_LAT"],self.data["TL_LON"],self.data["BR_LAT"],self.data["BR_LON"])
        self.data["CENT"] = f"{center_lat}\n{center_lon}"
        debug_print("[id]")
        debug_print(self.data["ID"])

        specific_data = get_result_by_id(search_id=int(self.data["ID"]))
        debug_print("[pop, pop/km]")
        debug_print(specific_data)
        # -------------------------------------------------
        tk.Label(self.frame_text, text=f"Latitude 1: {self.data["TL_LAT"]}", anchor="w",justify="left",bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 1))

        tk.Label(self.frame_text, text=f"Longitude 1: {self.data["TL_LON"]}", anchor="w",justify="left",bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 1))

        tk.Label(self.frame_text, text=f"Latitude 2: {self.data["BR_LAT"]}", anchor="w",justify="left",bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 1))

        tk.Label(self.frame_text, text=f"Longitude 2: {self.data["BR_LON"]}", anchor="w",justify="left",bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 1))

        tk.Label(self.frame_text, text=f"Center:\n {self.data["CENT"]}", justify="left",bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 2))

        tk.Label(self.frame_text, text=f"Estimativa populacional: {specific_data[0]}", bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 1))

        tk.Label(self.frame_text, text=f"Densidade populacional aproximada:\n {specific_data[1]}", bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 1))


        self.image_container = tk.LabelFrame(self,width=250,bg="#FFD8E6")
        self.image_container.pack(padx=(20, 20), pady=(20, 15), side="left", fill="both", expand=True)



        fp = f"media/processed/{slug}.png"

        img = Image.open(fp)
        self.rawphoto = ImageTk.PhotoImage(img)


        self.image= tk.Label(self.image_container,image=self.rawphoto)
        self.image.pack()
    #     self.bind("<Configure>", self.on_resize)
    # def on_resize(self,event):
    #     # CRITICAL: Filter out sub-widget resize events
    #     print(f"Window resized to: {event.width}x{event.height}")
    #     debug_print(event)





class MainMapWindow(tk.Tk):
    def __init__(self):
        debug_print("setting up main window")
        super().__init__()
        self.title("Main Window")
        self.geometry("1000x650")

        self.configure(bg="#B0E0E6")
        self.start_x = None
        self.start_y = None
        self.rect_id = None

        self.poligono_selecao = None
        self.selection_marker = None

        self.frame_lateral = tk.LabelFrame( width=250, bg="#ADD8E6")
        self.frame_lateral.pack(side="right", fill="y", pady=(20, 15), padx=(0, 20))
        self.frame_lateral.pack_propagate(False)

        self.frame_text = tk.Frame(self.frame_lateral, bg="#ADD8E6")
        self.frame_text.pack(expand=True)

        

        # -------------------------------------------------
        tk.Label(self.frame_text, text="Latitude 1:", bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 2))
        self.set_lat1 = tk.Entry(self.frame_text, justify="center")
        self.set_lat1.pack(pady=(0, 5))

        tk.Label(self.frame_text, text="Longitude 1:", bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 2))
        self.set_lon1 = tk.Entry(self.frame_text, justify="center")
        self.set_lon1.pack(pady=(0, 5))

        tk.Label(self.frame_text, text="Latitude 2:", bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 2))
        self.set_lat2 = tk.Entry(self.frame_text, justify="center")
        self.set_lat2.pack(pady=(0, 5))

        tk.Label(self.frame_text, text="Longitude 2:", bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 2))
        self.set_lon2 = tk.Entry(self.frame_text, justify="center")
        self.set_lon2.pack(pady=(0, 10))

        self.button_marcar = tk.Button(self.frame_text, text="Selecionar Região",
                                       command=self.capturar_entradas_e_desenhar)
        self.button_marcar.pack(pady=(0, 10))

        self.button_remove = tk.Button(self.frame_text, text="Apagar marcação", command= self.limpar_marcacao)
        self.button_remove.pack(pady=(0, 40))

        self.button_confirm = tk.Button(self.frame_text, text="pesquisar", command= self.search_selection)
        self.button_confirm.pack(pady=(0, 40))

        self.button_relat = tk.Button(self.frame_text, text="relatorio", command= self.relatorio)
        self.button_relat.pack(pady=(0, 40))

        # -------------------------------------------------
        # -------------------------------------------------

        # self.button_area = tk.Button(self.frame_text, text="Selecionar Area", command=self.ativar_selecao)
        # self.button_area.pack(pady=(0,50))

        # Entradas de Texto
        tk.Label(self.frame_text, text="Latitude:", bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 2))
        self.set_lat = tk.Entry(self.frame_text, justify="center")
        self.set_lat.pack(pady=(0, 5))

        tk.Label(self.frame_text, text="Longitude:", bg="#ADD8E6", font=("Arial", 9, "bold")).pack(pady=(0, 2))
        self.set_long = tk.Entry(self.frame_text, justify="center")
        self.set_long.pack(pady=(0, 5))

        # Botão
        self.button_search = tk.Button(self.frame_text, text="Buscar Coordenadas", command=self.get_cords)
        self.button_search.pack()


        # --- Mapa ---
        self.map_label = tk.LabelFrame( width=250)
        self.map_label.pack(padx=(20, 20), pady=(20, 15), side="left", fill="both", expand=True)

        self.map_widget = tkintermapview.TkinterMapView(self.map_label, width=1000, height=800)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=y&hl=pt-BR&x={x}&y={y}&z={z}&s=Ga")
        self.map_widget.set_position(-28.9510156, -49.4678388)  # Posição inicial (UFSC-Ararangua)
        self.map_widget.set_zoom(18)
        self.map_widget.pack(fill="both", expand=True)

        self.map_widget.add_right_click_menu_command(label="Add Marker 1 (top left)",
                                                command=lambda coords: self.add_marker_event(coords,1),
                                                pass_coords=True)
        self.map_widget.add_right_click_menu_command(label="Add Marker 2 (bottom right)",
                                                command=lambda coords: self.add_marker_event(coords,2),
                                                pass_coords=True)

        # self.bind("<Configure>", self.on_resize)
        debug_print("main window ready")

    def search_selection(self):
        debug_print("attempting to make new request")
        if hasattr(self, 'poligono_selecao') and self.poligono_selecao:
            debug_print("has selection")
        else:
            debug_print("selection missing, aborting")
            return
        #warn this is dangerous and can break EASILY
        lat1 = float(self.set_lat1.get())
        lon1 = float(self.set_lon1.get())
        lat2 = float(self.set_lat2.get())
        lon2 = float(self.set_lon2.get())

        slug = get_map_image(lat1,lon1,lat2,lon2)

        DetailView(parent=self, slug=slug)

    # def on_resize(self,event):
    #     # CRITICAL: Filter out sub-widget resize events
    #     print(f"Window resized to: {event.width}x{event.height}")
    #     debug_print(event)



    def relatorio(self):
        Relatorio(parent=self)






    def add_marker_event(self,coords,id):
        debug_print(f"coordinate selected {id}: {coords}")
        if id == 1:
            self.set_lat1.delete(0, tk.END)
            self.set_lat1.insert(0, str(coords[0]))
            self.set_lon1.delete(0, tk.END)
            self.set_lon1.insert(0, str(coords[1]))
        else:
            self.set_lat2.delete(0, tk.END)
            self.set_lat2.insert(0, str(coords[0]))
            self.set_lon2.delete(0, tk.END)
            self.set_lon2.insert(0, str(coords[1]))


    def get_cords(self):
        debug_print("moving map to set coords")
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
            # TODO: throw error popup, user feedback should not rely on the terminal

    def desenhar_regiao_geografica(self, lat1, lon1, lat2, lon2):
        debug_print("drawing selection")
        if hasattr(self, 'poligono_selecao') and self.poligono_selecao:
            self.poligono_selecao.delete()

        ponto_superior_esquerdo = (lat1, lon1)
        ponto_superior_direito = (lat1, lon2)
        ponto_inferior_direito = (lat2, lon2)
        ponto_inferior_esquerdo = (lat2, lon1)

        # make selection a square (more accurate to what google actually requests
        cent_lat = (lat1+lat2)/2
        cent_lon = (lon1+lon2)/2

        if self.selection_marker is not None:
            self.selection_marker.delete()
            self.selection_marker = None


        self.selection_marker = self.map_widget.set_marker(cent_lat, cent_lon, text="center")


        selection_path = [
            ponto_superior_esquerdo,
            ponto_superior_direito,
            ponto_inferior_direito,
            ponto_inferior_esquerdo
        ]

        self.poligono_selecao = self.map_widget.set_polygon(
            selection_path,
            fill_color=None,  # Sem preenchimento interno (transparente)
            outline_color="red",  # Cor da borda do quadrado
            border_width=3,  # Espessura da linha
            name="regiao_marcada"
        )




    def capturar_entradas_e_desenhar(self):
        debug_print("getting selection data")
        try:
            lat1 = float(self.set_lat1.get())
            lon1 = float(self.set_lon1.get())
            lat2 = float(self.set_lat2.get())
            lon2 = float(self.set_lon2.get())

            self.desenhar_regiao_geografica(lat1, lon1, lat2, lon2)

        except ValueError:
            print(
                "Erro de digitação: Certifique-se de preencher todos os campos apenas com números e usar ponto (ex: -27.59) em vez de vírgula.")
            # TODO:  Line 115

    def limpar_marcacao(self):
        debug_print("delete selection")
        if hasattr(self, 'poligono_selecao') and self.poligono_selecao:
            self.poligono_selecao.delete()
            self.poligono_selecao = None

        if hasattr(self, 'rect_id') and self.rect_id:
            self.map_widget.canvas.delete(self.rect_id)
            self.rect_id = None

        self.selection_marker.delete()
        self.selection_marker = None

        self.set_lat1.delete(0, tk.END)
        self.set_lon1.delete(0, tk.END)
        self.set_lat2.delete(0, tk.END)
        self.set_lon2.delete(0, tk.END)

        print("Marcação e coordenadas apagadas com sucesso.")
        # TODO:  Line 115 maybe remove anyway

    #todo lock coordinate editing when selection exists
    




class Relatorio(tk.Toplevel):
    print("chamou relatorio")
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Relatorio")
        self.geometry("833x558")
        self.configure(bg="#B0E0E6")


        self.frames_da_tela()
        self.lista_frame2()


        dados_recebidos = get_all_history()
       # dados_recebidos =  [
         #   (1, -28.9344, -49.4958, -28.6760, -49.3723), # Araranguá -> Criciúma
         #   (2, -27.5969, -48.5495, -28.4820, -49.0061), # Floripa -> Tubarão
         #   (3, -29.0084, -49.5638, -26.3044, -48.8456), # Sombrio -> Joinville
         #   (4, -28.9344, -49.4958, -30.0346, -51.2177), # Araranguá -> Porto Alegre
        #    (5, -25.4284, -49.2733, -27.5969, -48.5495), # Curitiba -> Floripa
        #    (6, -28.2612, -49.1601, -28.9344, -49.4958), # Laguna -> Araranguá
         #   (7, -26.9109, -49.0661, -27.5969, -48.5495)  # Blumenau -> Floripa
        #]
        self.preencher_lista(dados_recebidos)

    def frames_da_tela(self):
        self.frame_2 = tk.Frame(self, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.pack(fill="both", expand=True)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3,
                                     column=("col1", "col2", "col3", "col4","col5"),show="headings")

        self.listaCli.heading("#1", text="Slug")
        self.listaCli.heading("#2", text="Latitude1")
        self.listaCli.heading("#3", text="Longitude1")
        self.listaCli.heading("#4", text="Latitude2")
        self.listaCli.heading("#5", text="Longitude2")

        self.listaCli.column("#1", width=100)
        self.listaCli.column("#2", width=100)
        self.listaCli.column("#3", width=100)
        self.listaCli.column("#4", width=100)
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient="vertical")
        # self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.01, relheight=0.85)

        self.listaCli.bind("<Double-1>", self.click_list)

    def preencher_lista(self, dados):
        
        for linha_antiga in self.listaCli.get_children():
            self.listaCli.delete(linha_antiga)

        for registro in dados:
            self.listaCli.insert("", "end", values=registro)

    def click_list(self, event):

        selecionado = self.listaCli.selection()

        if not selecionado:
            return
        

        valores_da_linha = self.listaCli.item(selecionado[0], "values")


        DetailView(parent=self, slug=valores_da_linha[0])

       
if __name__ == "__main__":
    app = MainMapWindow()
    app.mainloop()
