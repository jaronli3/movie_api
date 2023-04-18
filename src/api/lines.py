from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

import operator

router = APIRouter()

@router.get("/lines/{movie_id}", tags=["lines"])
def get_line(movie_id: str):
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
    movie = db.movies.get(movie_id)
    if movie:
        top_chars = [
            {"character_id": c.id, "character": c.name, "num_lines": c.num_lines}
            for c in db.characters.values()
            if c.movie_id == movie_id
        ]
        top_chars.sort(key=lambda c: c["num_lines"], reverse=True)

        result = {
            "movie_id": movie_id,
            "title": movie.title,
            "top_characters": top_chars[0:5],
        }
        return result

    raise HTTPException(status_code=404, detail="movie not found.")