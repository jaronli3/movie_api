from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

import operator

router = APIRouter()

@router.get("/lines/{line_id}", tags=["lines"])
def get_line(line_id: int):
    """
    This endpoint returns a single line by its identifier. For each line it returns:
    * `line_id`: the internal id of the line.
    * `line_text`: The text of the line.
    * 'movie': The movie the line came from.
    * `characters_involved`: A list of characters that were involved in that conversation. 

    Each character is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    * 'age': The age of the character.

    """

    json = None
    movie_id = None
    convo_id = None
    character_1 = None
    character_2 = None

    for line in db.lines:
        if int(line["line_id"]) == line_id:
            json = {}
            json["line_id"] = line_id
            json["line_text"] = line["line_text"]
            # movie_id = line["movie_id"]
            # convo_id = line["conversation_id"]
            # character_1 = line["character_id"]
            break

    if json is None:
        raise HTTPException(status_code=404, detail="line not found.")

    # for movie in db.movies:
    #     if movie_id == movie["movie_id"]:
    #         json["movie"] = movie["title"]
    
    # for convo in db.conversations:
    #     if convo["character1_id"] == character_1:
    #         character_2 = convo["character2_id"]
    #     elif convo["character2_id"] == character_1:
    #         character_2 = convo["character1_id"]


    # lst = []
    
    # for char in db.characters:
    #     char_json = {}
    #     if char["character_id"] == character_1:
    #         char_json["character_id"] = char["character_id"]
    #         char_json["name"] = char["name"]
    #         if character["gender"] == "":
    #           char_json["gender"] = None
    #         else:
    #           char_json["gender"] = char["gender"]
    #         char_json["age"] = int(char["age"])
    #         lst.append(char_json)
    #     elif char["character_id"] == character_2:
    #         char_json["character_id"] = char["character_id"]
    #         char_json["name"] = char["name"]
    #         if character["gender"] == "":
    #           char_json["gender"] = None
    #         else:
    #           char_json["gender"] = char["gender"]
    #         char_json["age"] = int(char["age"])
    #         lst.append(char_json)

    # json["characters_involved"] = lst

    return json

# Add get parameters
@router.get("/lines/", tags=["lines"])
def list_lines(
    line: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
):
    """
    This endpoint returns a list of lines. For each line it returns:
    * `line_id`: the internal id of the line. 
    * `line_text`: The text of the line.
    * `movie`: The movie the line came from.
    * 'characters_involved': A list of characters that were involved in that conversation. 

    Each character is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    * 'age': The age of the character.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    json = []

    for movies in db.movies:
      if name.lower() in movies["title"]:
          dictionary = {}
          dictionary["movie_id"] = int(movies["movie_id"])
          dictionary["movie_title"] = movies["title"]
          dictionary["year"] = movies["year"]
          dictionary["imdb_rating"] = float(movies["imdb_rating"])
          dictionary["imdb_votes"] = int(movies["imdb_votes"])
          json.append(dictionary)

    if sort.lower() == "movie_title":
      return sorted(json, key=operator.itemgetter('movie_title'))[offset:limit + offset]
    elif sort.lower() == "year":
      return sorted(json, key=operator.itemgetter('year'))[offset:limit + offset]
    elif sort.lower() == "rating":
      return sorted(json, key=operator.itemgetter('imdb_rating'), reverse = True)[offset:limit + offset]

    return json[offset:limit + offset]
