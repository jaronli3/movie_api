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
    return None