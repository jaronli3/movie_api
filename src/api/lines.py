from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

import operator

router = APIRouter()
def get_top_conv_characters(character):
    c_id = character.id
    movie_id = character.movie_id
    all_convs = filter(
        lambda conv: conv.movie_id == movie_id
        and (conv.c1_id == c_id or conv.c2_id == c_id),
        db.conversations.values(),
    )
    line_counts = Counter()

    for conv in all_convs:
        other_id = conv.c2_id if conv.c1_id == c_id else conv.c1_id
        line_counts[other_id] += conv.num_lines

    return line_counts.most_common()


@router.get("/characters/{id}", tags=["characters"])
def get_character(id: int):
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

    character = db.characters.get(id)

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

# @router.get("/lines/{line_id}", tags=["lines"])
# def get_line(line_id: str):
#     """
#     This endpoint returns a single line by its identifier. For each line it returns:
#     * `line_id`: the internal id of the line.
#     * `line_text`: The text of the line.
#     * `characters_involved`: A list of characters that were involved in that conversation. 

#     Each character is represented by a dictionary with the following keys:
#     * `character_id`: the internal id of the character.
#     * `character`: The name of the character.
#     * `gender`: The gender of the character.
#     """
    # line = db.lines.get(line_id)
    # print(line)
    # if line:
    #     json = {"line_id": line.id, "line_text": line.line_text}
    #     return json
    
    # raise HTTPException(status_code=404, detail="line not found.")