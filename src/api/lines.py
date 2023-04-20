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

class char_lines_sort_options(str, Enum):
    line_text = "line_text"

@router.get("/lines_spoken_by_character/", tags=["lines"])
def get_char_lines(character_name: str, limit: int = Query(50, ge=1, le=250), offset: int = Query(0, ge=0)):
    """
    This endpoint returns lines spoken by the given character. For each line it returns:
    * `character_id`: the id of the character.
    * `character_name`: Name of the character.
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

    json = []
    char = None
    for character in db.characters:
        char1 = db.characters.get(character)
        if character_name.lower() == char1.name.lower():
            char = char1
            break
    
    if char:
        for line_id in db.lines:
            new_line = db.lines.get(line_id)
            if new_line.c_id == char.id:
                dictionary = {}
                dictionary["character_id"] = char.id
                dictionary["character_name"] = char.name
                movie = db.movies.get(char.movie_id)
                dictionary["movie_id"] = movie.id
                dictionary["movie_title"] = movie.title
                dictionary["line_text"] = new_line.line_text
                convo = new_line.conv_id
                conversation = db.conversations.get(convo)
                other_char = None
                if conversation.c1_id == char.id:
                    other_char = conversation.c2_id
                elif conversation.c2_id == char.id:
                    other_char = conversation.c1_id
                speaking_to_character = db.characters.get(other_char)
                other_char_dictionary = {}
                other_char_dictionary["character_id"] = speaking_to_character.id
                other_char_dictionary["character_name"] = speaking_to_character.name
                other_char_dictionary["gender"] = speaking_to_character.gender
                other_char_dictionary["age"] = speaking_to_character.age
                dictionary["speaking to this character"] = other_char_dictionary
                json.append(dictionary)
    
    return sorted(json, key=operator.itemgetter('line_text'))[offset:limit + offset]

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