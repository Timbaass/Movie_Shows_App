# MovieShowManager
import os
import json


class MovieShowManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.movies_shows = self.load_data()  # Başlangıçta veriyi yükle

    # Veri dosyasını kontrol et ve veriyi yükle
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                return json.load(file)
        return []

    # Veriyi JSON dosyasına kaydet
    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump(self.movies_shows, file)

    def add_item(self, name, type_):
        if name != "":
            new_item = {
                "name": name,
                "type": type_,
                "status": "İzlenmedi",
                "rating": 0
            }
            self.movies_shows.append(new_item)
            self.save_data()

    def delete_item(self, name):
        for movie in self.movies_shows:
            if movie["name"] == name:
                self.movies_shows.pop(self.movies_shows.index(movie))
                break
        self.save_data()

    # Durum güncelleme
    def update_status(self, name, status):
        for movie in self.movies_shows:
            if movie['name'] == name:
                movie['status'] = status
                break
        self.save_data()

    # Yıldız değerlendirme
    def update_rating(self, name, rating):
        for movie in self.movies_shows:
            if movie['name'] == name:
                movie['rating'] = rating
                break
        self.save_data()

    def get_movies(self):
        return self.movies_shows
