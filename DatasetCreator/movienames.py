import imdb


def get_best_hindi_movies():
    ia = imdb.IMDb()

    # Search for Hindi movies
    search_results = ia.search_movie('Old Hindi Movies')

    hindi_movies = []
    for result in search_results:
        hindi_movies.append(result)


    # Sort movies by rating
    sorted_movies = sorted(hindi_movies, key=lambda x: x.get('rating', 0), reverse=True)

    return sorted_movies


def format_movie_titles(movie_list):
    titles = [movie['title'] for movie in movie_list]
    return ', '.join(titles)


if __name__ == "__main__":
    # Get the list of best Hindi movies
    best_hindi_movies = get_best_hindi_movies()

    # Format the movie titles as comma-separated string
    movie_titles = format_movie_titles(best_hindi_movies)

    print("List of Best Hindi Movies:", movie_titles)
