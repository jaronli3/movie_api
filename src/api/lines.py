from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

import operator
import sqlalchemy

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

    line = sqlalchemy.select(db.lines.c.line_id, db.lines.c.line_text, db.lines.c.movie_id, db.lines.c.character_id, db.lines.c.conversation_id).where(db.lines.c.line_id == line_id)

    with db.engine.connect() as conn:
        line1 = conn.execute(line).fetchone()
        if line1:
            movie = sqlalchemy.select(db.movies.c.title).where(line1.movie_id == db.movies.c.movie_id)
            movie_title = conn.execute(movie).fetchone()
            title_name = movie_title.title
            speaker = sqlalchemy.select(db.chars.c.name, db.chars.c.gender, db.chars.c.age).where(line1.character_id == db.chars.c.character_id)
            speaker1 = conn.execute(speaker).fetchone()
            speaker_name = speaker1.name
            json = {
                "line_id": line1.line_id,
                "line_text": line1.line_text,
                "movie_title": title_name
            }
            lst = []
            speaker_dict = {
                "character_id": line1.character_id,
                "character name": speaker_name,
                "gender": speaker1.gender,
                "age": speaker1.age
            }

            conversation = sqlalchemy.select(db.convos.c.character1_id, db.convos.c.character2_id).where(line1.conversation_id == db.convos.c.conversation_id)
            conversation1 = conn.execute(conversation).fetchone()
            if conversation1.character1_id == line1.character_id:
                other_char_id = conversation1.character2_id
            elif conversation1.character2_id == line1.character_id:
                other_char_id = conversation1.character1_id

            other_character = sqlalchemy.select(db.chars.c.character_id, db.chars.c.name, db.chars.c.gender, db.chars.c.age).where(db.chars.c.character_id == other_char_id)
            other_char1 = conn.execute(other_character).fetchone()
            other_char_dict = {
                "character_id": other_char1.character_id,
                "character name": other_char1.name,
                "gender": other_char1.gender,
                "age": other_char1.age
            }
            
            lst.append(speaker_dict)
            lst.append(other_char_dict)
            json["characters involved"] = lst
            return json

        raise HTTPException(status_code=404, detail="line not found.")


class char_lines_sort_options(str, Enum):
    line_text = "line_text"


@router.get("/lines_spoken_by_character/", tags=["lines"])
def get_char_lines(char_id: int, limit: int = Query(50, ge=1, le=250), offset: int = Query(0, ge=0)):
    """
    This endpoint returns lines spoken by the given character. For each line it returns:
    * `character_id`: the id of the character.
    * `character_name`: Name of the character.
    * 'movie_id': Movie id of the movie.
    * 'movie_title': The movie the character spoke in.
    * `line_text`: The line the character said. 
    * `speaking to this character`: a dictionary of the character the given character is speaking to and
                                    their attributes.

    Each character the given character is speaking to will have the following keys in the dictionary:
    * `character_id`: the id of the character
    * `character_name`: the name of the character
    * `gender`: the gender of the character
    * `age`: the age of the character

    The results will be sorted by line_text in alphabetical order.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    
    stmt = (sqlalchemy.select(db.chars.c.character_id, db.chars.c.name, db.chars.c.movie_id).where(char_id == db.chars.c.character_id))
   
    with db.engine.connect() as conn:
        result = conn.execute(stmt).fetchone()
        if result:
            lines = (sqlalchemy.select(db.lines.c.movie_id, db.lines.c.line_text, db.lines.c.conversation_id).where(db.lines.c.character_id == char_id)
            .limit(limit)
            .offset(offset)
            .order_by(db.lines.c.line_text))

            lines1 = conn.execute(lines).fetchall()
            lst = []
            for x in lines1:
                line_text = x.line_text
                movie = sqlalchemy.select(db.movies.c.title).where(db.movies.c.movie_id == x.movie_id)
                movie1 = conn.execute(movie).fetchone()
                movie_title = movie1.title
                json = {"character_id": result.character_id, "character_name": result.name, "movie_id": result.movie_id, "movie_title": movie_title, "line_text": line_text}
                conversation = sqlalchemy.select(db.convos.c.character1_id, db.convos.c.character2_id).where(x.conversation_id == db.convos.c.conversation_id)
                conversation1 = conn.execute(conversation).fetchone()
                if char_id == conversation1.character1_id:
                    other_char = conversation1.character2_id
                    other_char1 = sqlalchemy.select(db.chars.c.character_id, db.chars.c.name, db.chars.c.gender, db.chars.c.age).where(db.chars.c.character_id == other_char)
                    other_character = conn.execute(other_char1).fetchone()
                    json1 = {"character_id": other_character.character_id, "character_name": other_character.name, "gender": other_character.gender, "age": other_character.age}
                    json["speaking to this character"] = json1
                elif char_id == conversation1.character2_id:
                    other_char = conversation1.character1_id
                    other_char2 = sqlalchemy.select(db.chars.c.character_id, db.chars.c.name, db.chars.c.gender, db.chars.c.age).where(db.chars.c.character_id == other_char)
                    other_character = conn.execute(other_char2).fetchone()
                    json1 = {"character_id": other_character.character_id, "character_name": other_character.name, "gender": other_character.gender, "age": other_character.age}
                    json["speaking to this character"] = json1
                lst.append(json)
            return lst

        raise HTTPException(status_code=404, detail="character not found.")
        
class line_sort_options(str, Enum):
    line_text = "line_text"
    movie = "movie"
    character = "character"
    line_id = "line_id"

@router.get("/lines/", tags=["lines"])
def get_lines(line_name: str, limit: int = Query(50, ge=1, le=250), offset: int = Query(0, ge=0), sort: line_sort_options = line_sort_options.line_text):
        """
    This endpoint returns a list of lines. For each line it returns:
    * `line_id`: the internal id of the line. 
    * `line_text`: The text of the line.
    * `movie`: The movie the line occurred in.
    * `character`: The character who said the line.
    * `speaking to`: The character who the speaker is speaking to.

    You can filter for lines whose text contain a string by using the
    `line` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `line_text` - Sort by line text alphabetically.
    * `movie` - Sort by movie alphabetically.
    * `character` - Sort by character alphabetically.
    * `line_id` - Sort by line_id in ascending order.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.

        """
    
        json = []
        for line in db.lines:
            new_line = db.lines.get(line)
            if line_name.lower() in new_line.line_text.lower():
                dictionary = {}
                dictionary["line_id"] = new_line.id
                dictionary["line_text"] = new_line.line_text
                movie = db.movies.get(new_line.movie_id)
                dictionary["movie"] = movie.title
                char = db.characters.get(new_line.c_id)
                dictionary["character"] = char.name
                convo = new_line.conv_id
                conversation = db.conversations.get(convo)
                other_char = None
                if conversation.c1_id == char.id:
                    other_char = conversation.c2_id
                    other_char1 = db.characters.get(other_char)
                    dictionary["speaking to"] = other_char1.name
                elif conversation.c2_id == char.id:
                    other_char = conversation.c1_id
                    other_char1 = db.characters.get(other_char)
                    dictionary["speaking to"] = other_char1.name
                json.append(dictionary)

        if sort.lower() == "line_text":
            return sorted(json, key=operator.itemgetter('line_text'))[offset:limit + offset]
        elif sort.lower() == "movie":
            return sorted(json, key=operator.itemgetter('movie'))[offset:limit + offset]
        elif sort.lower() == "character":
            return sorted(json, key=operator.itemgetter('character'))[offset:limit + offset]
        elif sort.lower() == "line_id":
            return sorted(json, key=operator.itemgetter('line_id'))[offset:limit + offset]

        return json[offset:limit + offset]