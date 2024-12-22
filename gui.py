from customtkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class User_Panel(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(height=500, corner_radius=15, bg_color="#F2F2F2")
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")

        self.title = CTkLabel(self, text="User Panel", font=("Roboto", 30, "bold"), text_color="#2c3e50")
        self.title.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 15))

        self.subtitle = CTkLabel(self, text="Welcome to the User Dashboard", font=("Arial", 14, "italic"),
                                 text_color="#7f8c8d")
        self.subtitle.grid(row=1, column=0, sticky="w", padx=20, pady=(5, 10))

        self.name_label = CTkLabel(self, text="Film/Dizi Adı:")
        self.name_label.grid(row=2, column=0, pady=5)
        self.name_entry = CTkEntry(self)
        self.name_entry.grid(row=3, column=0, pady=5)

        self.type_label = CTkLabel(self, text="Tür Seçin:")
        self.type_label.grid(row=4, column=0, pady=5)
        self.type_var = StringVar(value="Film")
        self.type_radio_movie = CTkRadioButton(self, text="Film", variable=self.type_var, value="Film")
        self.type_radio_movie.grid(row=5, column=0, pady=5)
        self.type_radio_show = CTkRadioButton(self, text="Dizi", variable=self.type_var, value="Dizi")
        self.type_radio_show.grid(row=6, column=0, pady=5)

        self.add_button = CTkButton(self, text="Ekle")
        self.add_button.grid(row=7, column=0, pady=10)

        self.status_label = CTkLabel(self, text="Durum Seçin:")
        self.status_label.grid(row=8, column=0, pady=5)
        self.status_var = StringVar(value="İzlenmedi")
        self.status_var_not_watched = CTkRadioButton(self, text="İzlenmedi", variable=self.status_var, value="İzlenmedi")
        self.status_var_watching = CTkRadioButton(self, text="İzleniyor", variable=self.status_var, value="İzleniyor")
        self.status_var_watched = CTkRadioButton(self, text="İzlendi", variable=self.status_var, value="İzlendi")
        self.status_var_not_watched.grid(row=9, column=0, pady=5)
        self.status_var_watching.grid(row=10, column=0, pady=5)
        self.status_var_watched.grid(row=11, column=0, pady=5)

        self.update_status_button = CTkButton(self, text="Durumu Güncelle")
        self.update_status_button.grid(row=12, column=0, pady=10)

        self.rating_label = CTkLabel(self, text="Yıldız Değerlendirme (1-5):")
        self.rating_label.grid(row=13, column=0, pady=5)
        self.rating_var = IntVar(value=0)
        self.rating_scale = CTkSlider(self, from_=1, to=5, variable=self.rating_var)
        self.rating_scale.grid(row=14, column=0, pady=5)

        self.update_rating_button = CTkButton(self, text="Yıldızı Güncelle")
        self.update_rating_button.grid(row=15, column=0, pady=5)

        self.delete_movie_show_button = CTkButton(self, text="Sil")
        self.delete_movie_show_button.grid(row=16, column=0, pady=5)


class Movie_Tabel(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(height=500, corner_radius=15, bg_color="#F2F2F2")
        self.grid(row=0, column=1, padx=20, pady=20, sticky="nswe")

        # Treeview için stil oluşturma
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 14, "bold"), foreground="#2c3e50", background="#dfe3e8")
        self.style.configure("Treeview", font=("Arial", 12), rowheight=30, background="#f9f9f9", foreground="#2c3e50")
        self.style.map("Treeview", background=[('selected', '#A9D0F5')])  # Seçili satırın rengi

        # Tabloyu oluşturma
        self.columns = ("Name", "Type", "Status", "Rating")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", style="Treeview")
        self.tree.heading("Name", text="Film/Dizi Adı")
        self.tree.heading("Type", text="Tür")
        self.tree.heading("Status", text="Durum")
        self.tree.heading("Rating", text="Yıldız")

        # Treeview'i ekrana yerleştirme
        self.tree.pack(fill=tk.BOTH, expand=True)


class App(CTk):
    def __init__(self, data_manager):
        super().__init__()

        self.data_manager = data_manager
        self.title("Film/Dizi İzleme Paneli")
        self.geometry("1200x700")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        self.user_panel = User_Panel(self)
        self.movie_tabel = Movie_Tabel(self)

        self.user_panel.add_button.configure(command=self.add_item)
        self.user_panel.update_status_button.configure(command=self.update_status)
        self.user_panel.update_rating_button.configure(command=self.update_rating)
        self.user_panel.delete_movie_show_button.configure(command=self.delete_movie_show)
        self.update_table()

    def update_table(self):
        for row in self.movie_tabel.tree.get_children():
            self.movie_tabel.tree.delete(row)
        for movie in self.data_manager.get_movies():
            self.movie_tabel.tree.insert(
                "", "end", values=(movie["name"], movie["type"], movie["status"], movie["rating"])
            )

    def add_item(self):
        name = self.user_panel.name_entry.get()
        type_ = self.user_panel.type_var.get()
        if name == "":
            messagebox.showerror("Hata", "Film/Dizi Adı boş bırakılmamalı!")
        else:
            messagebox.showinfo("Başarılı", f"{type_.capitalize()} başarıyla eklendi.")
        self.data_manager.add_item(name, type_)
        self.update_table()

    def update_status(self):
        selected_item = self.movie_tabel.tree.selection()
        if selected_item:
            selected_item = selected_item[0]  # Selektif item'a doğru erişim sağla
            item = self.movie_tabel.tree.item(selected_item)
            item_name = item['values'][0]
            status = self.user_panel.status_var.get()
            self.data_manager.update_status(item_name, status)
            self.update_table()

    def update_rating(self):
        selected_item = self.movie_tabel.tree.selection()
        if selected_item:
            selected_item = selected_item[0]  # Selektif item'a doğru erişim sağla
            item = self.movie_tabel.tree.item(selected_item)
            item_name = item['values'][0]
            rating = self.user_panel.rating_var.get()
            self.data_manager.update_rating(item_name, rating)
            self.update_table()

    def delete_movie_show(self):
        selected_item = self.movie_tabel.tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            item = self.movie_tabel.tree.item(selected_item)
            item_name = item["values"][0]
            self.data_manager.delete_item(item_name)
            self.update_table()



