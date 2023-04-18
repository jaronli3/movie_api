from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

import operator

router = APIRouter()

@router.get("/lines/{id}", tags=["lines"])
def get_line(id: str):
    """
    This endpoint returns a single line by its identifier. For each line it returns:
    * `line_id`: the internal id of the line.
    * `line_text`: The text of the line.
    * `characters_involved`: A list of characters that were involved in that conversation. 

    Each character is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    """
    
    # movie_id = None
    # convo_id = None
    # character_1 = None
    # character_2 = None

    # line = db.lines.get("50")
    # if line:
    #     json = {}
    #     json["line_id"] = line
    #     return json
    for line in db.lines:
        if line["line_id"] == id:
            json = {}
            json["line_id"] = line["line_id"]
            json["line_text"] = line["line_text"]
            movie_id = line["movie_id"]
            convo_id = line["conversation_id"]
            character_1 = line["character_id"]
            return json

    
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