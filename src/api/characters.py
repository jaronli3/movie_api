from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

import operator
router = APIRouter()


@router.get("/characters/{id}", tags=["characters"])
def get_character(id: str):
    """
    This endpoint returns a single character by its identifier. For each character
    it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `gender`: The gender of the character.
    * `top_conversations`: A list of characters that the character has the most
      conversations with. The characters are listed in order of the number of
      lines together. These conversations are described below.

    Each conversation is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    * `number_of_lines_together`: The number of lines the character has with the
      originally queried character.
    """

    json = None

    for character in db.characters:
        if character["character_id"] == id:
            json = {}
            json["character_id"] = int(id)
            json["character"] = character["name"]
            json["movie"] = character["movie_id"]
            if character["gender"] == "":
              json["gender"] = None
            else:
              json["gender"] = character["gender"]
            break

    if json is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    for movie in db.movies:
      if movie["movie_id"] == json["movie"]:
        json["movie"] = movie["title"]
        break
    
    top_convo_dict = {}
    top_convo_dict2 = {}
    char_found = False
    current_convo_id = None
    curr_char = None
    
    for conversation in db.conversations:
      if conversation["character1_id"] == id:
        char_found = True
        current_convo_id = conversation["conversation_id"]
        curr_char = conversation["character2_id"]
        if conversation["character2_id"] not in top_convo_dict:
          top_convo_dict[current_convo_id] = curr_char
      elif conversation["character2_id"] == id:
        char_found = True
        current_convo_id = conversation["conversation_id"]
        curr_char = conversation["character1_id"]
        if conversation["character1_id"] not in top_convo_dict:
          top_convo_dict[current_convo_id] = curr_char

    
    for conv in top_convo_dict:
      for line in db.lines:
        if line["conversation_id"] == conv:
          if top_convo_dict[conv] not in top_convo_dict2:
            top_convo_dict2[top_convo_dict[conv]] = 1
          else:
            top_convo_dict2[top_convo_dict[conv]] += 1

    top_convo_3 = {}

    # sorted_top_convo_2 = dict(sorted(top_convo_dict2.items(), key=operator.itemgetter(1),reverse=True))
    sorted_top_convo_2 = dict(sorted(top_convo_dict2.items(), key = lambda x:x[1], reverse = True))

    json["top_conversations"] = sorted_top_convo_2



    return json

class character_sort_options(str, Enum):
    character = "character"
    movie = "movie"
    number_of_lines = "number_of_lines"


@router.get("/characters/", tags=["characters"])
def list_characters(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: character_sort_options = character_sort_options.character,
):
    """
    This endpoint returns a list of characters. For each character it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `number_of_lines`: The number of lines the character has in the movie.

    You can filter for characters whose name contains a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `character` - Sort by character name alphabetically.
    * `movie` - Sort by movie title alphabetically.
    * `number_of_lines` - Sort by number of lines, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    json = None
    return json
