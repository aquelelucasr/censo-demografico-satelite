from tkinter import *

class Menu_lateral(Frame):
    def __init__(self, parent):

        super().__init__(parent, bg="#108cff", width=200,height=500)

        self.pack_propagate(False)

        self.sidebar_expand = True
        self.toggle_button = Button(self, text="menu", bg="#034787", fg="white", cursor="hand2",  font=("Arial", 16), relief = "flat", command=self.toggle_sidebar)

        self.toggle_button.pack(pady=10, padx=10, fill="x", anchor="w")

        self.nav_buttons = []
        for text in["Home", "Profile", "Settings"]:
            btn = Button(self, text=text, bg="#034787", fg="white", font=("Arial", 14), relief="flat", cursor="hand2", anchor="w")
            self.nav_buttons.append(btn)

        btn_close = Button(self, text="Close", bg="#034787", fg="red", font=("Arial",14), relief="flat", cursor="hand2", anchor="w", command=self.master.destroy)
        btn_close.pack(fill="x", pady=5, padx=10)
        self.nav_buttons.append(btn_close)
        self.toggle_sidebar()

    def toggle_sidebar(self):

        if self.sidebar_expand:
            self.config(width=50)
            self.toggle_button.config(text="☰", font=("Arial",12))
            for btn in self.nav_buttons:
                btn.pack_forget()
            self.sidebar_expand = False
           
        else:
            self.config(width=200)
            self.toggle_button.config(text="☰", font=("Arial", 16))
            for btn in self.nav_buttons:
                btn.pack(fill="x", pady=5, padx=10)
            self.sidebar_expand = True
            
       
