from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

import operator

router = APIRouter()

@router.get("/lines/{line_id}", tags=["lines"])
def get_line(line_id: str):
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
    character = db.characters.get(line_id)

    if character:
        movie = db.movies.get(character.movie_id)
        result = {
            "character_id": character.id,
            "character": character.name,
            "movie": movie and movie.title,
            "gender": character.gender,
            "top_conversations": (
                {
                    "character_id": other_id,
                    "character": db.characters[other_id].name,
                    "gender": db.characters[other_id].gender,
                    "number_of_lines_together": lines,
                }
                for other_id, lines in get_top_conv_characters(character)
            ),
        }
        return result

    raise HTTPException(status_code=404, detail="character not found.")
    # line = db.lines.get(line_id)
    # print(line)
    # if line:
    #     json = {"line_id": line.id, "line_text": line.line_text}
    #     return json
    
    # raise HTTPException(status_code=404, detail="line not found.")