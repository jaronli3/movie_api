from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()


# include top 3 actors by number of lines
@router.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: str):
    """
    This endpoint returns a single movie by its identifier. For each movie it returns:
    * `movie_id`: the internal id of the movie.
    * `title`: The title of the movie.
    * `top_characters`: A list of characters that are in the movie. The characters
      are ordered by the number of lines they have in the movie. The top five
      characters are listed.

    Each character is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `num_lines`: The number of lines the character has in the movie.

    """

    json = None

    for movie in db.movies:
        if movie["movie_id"] == movie_id:
            json = {}
            json["movie_id"] = int(movie_id)
            json["title"] = movie["title"]
            break

    if json is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    
    lst = []
    convo_dict = {}
    lines_dict = {}
    
    #gets characters in the movie
    for char in db.characters:
        if char["movie_id"] == movie_id:
            current_char_id = char["character_id"]
            lst.append(current_char_id)
    
    for char in lst:
        for line in db.lines:
            if line["character_id"] == char and line["movie_id"] == movie_id:
                if char not in lines_dict:
                    lines_dict[char] = 1
                else:
                    lines_dict[char] += 1


    json["top_conversations"] = sorted(lines_dict, key=operator.itemgetter(lines_dict.values()), reverse= True)
    # json["top_characters"] = lines_dict
    return json


class movie_sort_options(str, Enum):
    movie_title = "movie_title"
    year = "year"
    rating = "rating"


# Add get parameters
@router.get("/movies/", tags=["movies"])
def list_movies(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: movie_sort_options = movie_sort_options.movie_title,
):
    """
    This endpoint returns a list of movies. For each movie it returns:
    * `movie_id`: the internal id of the movie. Can be used to query the
      `/movies/{movie_id}` endpoint.
    * `movie_title`: The title of the movie.
    * `year`: The year the movie was released.
    * `imdb_rating`: The IMDB rating of the movie.
    * `imdb_votes`: The number of IMDB votes for the movie.

    You can filter for movies whose titles contain a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `movie_title` - Sort by movie title alphabetically.
    * `year` - Sort by year of release, earliest to latest.
    * `rating` - Sort by rating, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    json = None

    return json
