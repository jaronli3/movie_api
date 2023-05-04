from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter

from fastapi.params import Query
from src import database as db

import operator
import sqlalchemy

router = APIRouter()

def get_char_num_lines_tot():
  lines = sqlalchemy.select(db.lines.c.character_id)
  with db.engine.connect() as conn:
    dictionary = {}
    lines1 = conn.execute(lines).fetchall()
    for x in lines1:
      if x.character_id not in dictionary:
        dictionary[x.character_id] = 1
      elif x.character_id in dictionary:
        dictionary[x.character_id] +=1
  
  return dictionary

def get_top_conv(conn, char_id: int):
    conversations = sqlalchemy.select(db.convos.c.conversation_id,
                    db.convos.c.character1_id, 
                    db.convos.c.character2_id).where((db.convos.c.character1_id == char_id) | (db.convos.c.character2_id == char_id))

    filtered_conversations_table = conn.execute(conversations).fetchall()

    lines = sqlalchemy.select(db.lines.c.conversation_id)

    filtered_lines_table = conn.execute(lines).fetchall()

    line_counts = {}

    line_counts2 = {}
    lst = []

    #gets number of lines for a conversation_id
    for line in filtered_lines_table:
      if line.conversation_id not in line_counts:
        line_counts[line.conversation_id] = 1
      elif line.conversation_id in line_counts:
        line_counts[line.conversation_id] += 1
 
    #gets number of lines for each other_char
    for convo in filtered_conversations_table:
      if char_id == convo.character1_id:
        other_char = convo.character2_id     
        if other_char in line_counts2:
          line_counts2[other_char] += line_counts[convo.conversation_id]
        elif other_char not in line_counts2:
          line_counts2[other_char] = line_counts[convo.conversation_id]
      elif char_id == convo.character2_id:
        other_char = convo.character1_id
        if other_char in line_counts2:
          line_counts2[other_char] += line_counts[convo.conversation_id]
        elif other_char not in line_counts2:
          line_counts2[other_char] = line_counts[convo.conversation_id]
      
    for x, y in line_counts2.items():
      top_other_character = sqlalchemy.select(db.chars.c.character_id,
                              db.chars.c.name,
                              db.chars.c.gender).where(db.chars.c.character_id == x)

      top_other_char1 = conn.execute(top_other_character).fetchone()
      top_conversation_part = {"character_id": top_other_char1.character_id,
                                  "character": top_other_char1.name,
                                  "gender": top_other_char1.gender,
                                  "number_of_lines_together": y}
      lst.append(top_conversation_part)
    
    lst1 = sorted(lst, key=operator.itemgetter('number_of_lines_together'), reverse= True)
    return lst1


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
    
    current_character = sqlalchemy.select(db.chars.c.character_id,
                        db.chars.c.name,
                        db.chars.c.movie_id,
                        db.chars.c.gender).where(db.chars.c.character_id == id)

    with db.engine.connect() as conn:
      curr_char1 = conn.execute(current_character).fetchone()
      if curr_char1:
        mov_id = curr_char1.movie_id
        movie = sqlalchemy.select(db.movies.c.title).where(mov_id == db.movies.c.movie_id)
        movie1 = conn.execute(movie).fetchone()
        movie_title = movie1.title
        top_convos = get_top_conv(conn, id)

        json = {"character_id": id,
                "character": curr_char1.name,
                "movie": movie_title,
                "gender": curr_char1.gender,
                "top_conversations": top_convos}
        
        return json

      raise HTTPException(status_code=404, detail="character not found.")

class character_sort_options(str, Enum):
    character = "character"
    movie = "movie"
    number_of_lines = "number_of_lines"


@router.get("/characters/", tags=["characters"])
def list_characters(
    name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
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
    
    lines_dictionary = get_char_num_lines_tot()

    if sort is character_sort_options.character:
        order_by = db.chars.c.name
    elif sort is character_sort_options.movie:
        order_by = db.movies.c.title
    elif sort is character_sort_options.number_of_lines:
        num = sqlalchemy.case(lines_dictionary, value = db.chars.c.character_id,  else_ = 0).label('num')
        order_by = sqlalchemy.desc(num)
    else:
        assert False

    stmt = (
        sqlalchemy.select(db.chars.c.character_id, db.chars.c.name, db.chars.c.movie_id).select_from(db.chars.join(db.movies, db.movies.c.movie_id == db.chars.c.movie_id))
        .limit(limit)
        .offset(offset)
        .order_by(order_by, db.chars.c.character_id)
    )


    # filter only if name parameter is passed
    if name != "":
        stmt = stmt.where(db.chars.c.name.ilike(f"%{name}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        lst = []
        for row in result:
          curr_movie_id = row.movie_id
          stmt1 = sqlalchemy.select(db.movies.c.title).where(curr_movie_id == db.movies.c.movie_id)
          movie_title_table = conn.execute(stmt1).fetchone()
          num_lines = lines_dictionary[row.character_id]
          dictionary = {"character_id": row.character_id, "character": row.name, "movie": movie_title_table.title, "number_of_lines": num_lines}
          lst.append(dictionary)

    return lst
