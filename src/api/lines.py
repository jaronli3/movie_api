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
    * `speaker`: Character who said the line. 

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
                
        conversation = db.conversations.get(convo_id)
        if conversation.c1_id == char1:
            char2 = conversation.c2_id
        elif conversation.c2_id == char1:
            char2 = conversation.c1_id

        lst = []
        character1 = db.characters.get(char1)
        character2 = db.characters.get(char2)
        char1_json = {"character_id": character1.id, "character name": character1.name, "gender": character1.gender, "age": character1.age}
        char2_json = {"character_id": character2.id, "character name": character2.name, "gender": character2.gender, "age": character2.age}
        lst.append(char1_json)
        lst.append(char2_json)
        json["characters involved"] = lst
    
        return json
    
    raise HTTPException(status_code=404, detail="line not found.")