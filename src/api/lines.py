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
    * 'movie_title': The movie the line came from.
    * `characters_involved`: A list of characters that were involved in that conversation. 

    Each character is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    * 'age': The age of the character.
    """

    line = db.lines.get(line_id)
    if line:
        json = {}
        mov_id = None
        char1 = None
        char2 = None
        convo_id = None
        json["line_id"] = line.id
        json["line_text"] = line.line_text
        mov_id = line.movie_id
        char1 = line.c_id
        convo_id = line.conv_id
        movie = db.movies.get(mov_id)
        json["movie_title"] = movie.title
                

        # for convo in db.conversations:
        #     if convo_id == convo["id"]:
        #         if convo["character1_id"] == char1:
        #             char2 = convo["character2_id"]
        #         elif convo["character2_id"] == char1:
        #             char2 = convo["character1_id"]
        #         break
                
        # lst = []
        # for char in db.characters:
        #     char_json = {}
        #     if char["character_id"] == char1:
        #         char_json["character_id"] = char["character_id"]
        #         char_json["name"] = char["name"]
        #         if character["gender"] == "":
        #             char_json["gender"] = None
        #         else:
        #             char_json["gender"] = char["gender"]
        #         char_json["age"] = int(char["age"])
        #         lst.append(char_json)
        #     elif char["character_id"] == char2:
        #         char_json["character_id"] = char["character_id"]
        #         char_json["name"] = char["name"]
        #         if character["gender"] == "":
        #             char_json["gender"] = None
        #         else:
        #             char_json["gender"] = char["gender"]
        #         char_json["age"] = int(char["age"])
        #         lst.append(char_json)

        # json["characters involved"] = lst

        return json
    
    raise HTTPException(status_code=404, detail="line not found.")