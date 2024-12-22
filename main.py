from gui import App
from data_management import MovieShowManager

data_file = "movies_show.json"
movie_show_manager = MovieShowManager(data_file)

app = App(movie_show_manager)
app.mainloop()
