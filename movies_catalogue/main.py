from flask import Flask, render_template, request, make_response
import tmdb_client

app = Flask(__name__)

@app.route('/')
def homepage():
    movie_list_types = ["popular", "top_rated", "upcoming", "now_playing"]
    selected_list = request.args.get('list_type', "popular")
    if selected_list not in movie_list_types:
        selected_list = "popular"
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list,
                           movie_list_types=movie_list_types)


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    return render_template("movie_details.html", movie=details, cast=cast)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


if __name__ == '__main__':
    app.run(debug=True)
