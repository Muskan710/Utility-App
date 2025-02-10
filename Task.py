import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO
import random


class MovieApp:
    def __init__(self, root):
        self.api_key = "7bbd09f0c05289bd6ab26ee11af1a7bb"
        self.base_url = "https://api.themoviedb.org/3"

        self.root = root
        self.root.title("Movie Database App")
        self.root.geometry("900x800")

        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.welcome_frame = tk.Frame(self.root, bg="pink")
        self.welcome_frame.pack(fill="both", expand=True)

        title = tk.Label(
            self.welcome_frame,text="Welcome to the Movie Database App",
            font=("Time New Roman", 28, "bold"),bg="#ebc034",fg="#34c6eb",
        )
        title.pack(pady=50)

        explore_button = tk.Button(
            self.welcome_frame,
            text="Explore Different Movies",font=("Arial", 16, "bold"),command=self.start_app,bg="#ebc034",fg="#34c6eb", padx=20,pady=10,
        )
        explore_button.pack(pady=20)

    def start_app(self):
        self.welcome_frame.destroy()
        self.create_widgets()
        self.get_latest_movies()

    def create_widgets(self):
        title = tk.Label(
            self.root, text="Movie Database App", font=("Time New Roman", 24, "bold"), bg="#ebc034", fg="#34c6eb"
        )
        title.pack(fill=tk.X)

        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5, fill=tk.X)

        genre_label = tk.Label(filter_frame, text="Genre:")
        genre_label.pack(side=tk.LEFT, padx=5)

        self.genre_combo = ttk.Combobox(
            filter_frame,
            values=["All", "Action", "Comedy", "Drama", "Horror"],
            state="readonly",
        )
        self.genre_combo.current(0)
        self.genre_combo.pack(side=tk.LEFT, padx=5)

        year_label = tk.Label(filter_frame, text="Year:")
        year_label.pack(side=tk.LEFT, padx=5)

        self.year_entry = tk.Entry(filter_frame, width=10)
        self.year_entry.pack(side=tk.LEFT, padx=5)

        search_year_btn = tk.Button(
            filter_frame, text="Search by Genre/Year", command=self.search_movies
        )
        search_year_btn.pack(side=tk.LEFT, padx=5)

        search_name_label = tk.Label(filter_frame, text="Name:")
        search_name_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(filter_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(filter_frame, text="Search by Name", command=self.search_movies_by_name)
        search_btn.pack(side=tk.LEFT, padx=5)

        random_button = tk.Button(
            filter_frame, text="Random Movie", command=self.show_random_movie
        )
        random_button.pack(side=tk.LEFT, padx=20)

        grid_container = tk.Frame(self.root)
        grid_container.pack(pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(grid_container)
        self.scrollbar = ttk.Scrollbar(grid_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.movie_grid_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.movie_grid_frame, anchor="nw")

        self.movie_grid_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def get_latest_movies(self):
        url = f"{self.base_url}/movie/now_playing"
        params = {"api_key": self.api_key}

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.display_movies(data.get("results", []))
        else:
            messagebox.showerror("Error", "Failed to fetch latest movies.")

    def display_movies(self, movies):
        for widget in self.movie_grid_frame.winfo_children():
            widget.destroy()

        rows, cols = 0, 0
        for movie in movies:
            frame = tk.Frame(self.movie_grid_frame, relief=tk.RAISED, borderwidth=1)
            frame.grid(row=rows, column=cols, padx=10, pady=10)
            frame.bind("<Button-1>", lambda event, m=movie: self.display_movie_details(m))

            poster_path = movie.get("poster_path")
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}"
                response = requests.get(poster_url)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    poster_image = Image.open(image_data)
                    poster_photo = ImageTk.PhotoImage(poster_image)

                    poster_label = tk.Label(frame, image=poster_photo)
                    poster_label.image = poster_photo
                    poster_label.pack()

            title_label = tk.Label(frame, text=movie.get("title", "N/A"), wraplength=150, justify=tk.CENTER)
            title_label.pack(pady=5)

            cols += 1
            if cols == 4:
                cols = 0
                rows += 1

    def display_movie_details(self, movie):
        details_window = tk.Toplevel(self.root)
        details_window.title(movie.get("title", "N/A"))
        details_window.geometry("900x600")

        poster_path = movie.get("poster_path")
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w300{poster_path}"
            response = requests.get(poster_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                poster_image = Image.open(image_data)
                poster_photo = ImageTk.PhotoImage(poster_image)

                poster_label = tk.Label(details_window, image=poster_photo)
                poster_label.image = poster_photo
                poster_label.pack(pady=10)

        tk.Label(details_window, text=movie.get("title", "N/A"), font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(details_window, text=f"Release Date: {movie.get('release_date', 'N/A')}").pack(pady=5)
        tk.Label(details_window, text=f"Rating: {movie.get('vote_average', 'N/A')}/10").pack(pady=5)

        overview = tk.Text(details_window, wrap=tk.WORD, height=10, width=60)
        overview.insert(tk.END, movie.get("overview", "No description available."))
        overview.pack(pady=10)
        overview.config(state=tk.DISABLED)

    def search_movies(self):
        genre = self.genre_combo.get()
        year = self.year_entry.get()
        genre_map = {"Action": 28, "Comedy": 35, "Drama": 18, "Horror": 27}
        genre_id = genre_map.get(genre) if genre != "All" else None

        url = f"{self.base_url}/discover/movie"
        params = {"api_key": self.api_key}
        if genre_id:
            params["with_genres"] = genre_id
        if year.isdigit():
            params["primary_release_year"] = year

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.display_movies(data.get("results", []))
        else:
            messagebox.showerror("Error", "Failed to fetch movies based on criteria.")

    def search_movies_by_name(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a movie name to search.")
            return
        url = f"{self.base_url}/search/movie"
        params = {"api_key": self.api_key, "query": query}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.display_movies(data.get("results", []))
        else:
            messagebox.showerror("Error", "Failed to search for movies.")

    def show_random_movie(self):
        url = f"{self.base_url}/movie/popular"
        params = {"api_key": self.api_key}

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            movies = data.get("results", [])
            if movies:
                random_movie = random.choice(movies)
                self.display_movie_details(random_movie)
            else:
                messagebox.showinfo("No Movies", "No movies available.")
        else:
            messagebox.showerror("Error", "Failed to fetch popular movies.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
