from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

import operator

router = APIRouter()

@router.get("/lines/{id}", tags=["lines"])
def get_line_by_character(id: str):
    """
    This endpoint returns line(s) spoken by the character given through their character_id. For each line it returns:
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
    
    char = db.characters.get(id)

    if char:
        json = {}
        json["movie"] = char["name"]
        return json

    if json is None:
        raise HTTPException(status_code=404, detail="line not found.")
    
    return json