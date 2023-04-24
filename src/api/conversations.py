from fastapi import APIRouter
from src import database as db
from pydantic import BaseModel
from typing import List
from datetime import datetime


# FastAPI is inferring what the request body should look like
# based on the following two classes.
class LinesJson(BaseModel):
    character_id: int
    line_text: str


class ConversationJson(BaseModel):
    character_1_id: int
    character_2_id: int
    lines: List[LinesJson]


router = APIRouter()


@router.post("/movies/{movie_id}/conversations/", tags=["movies"])
def add_conversation(movie_id: int, conversation: ConversationJson):
    """
    This endpoint adds a conversation to a movie. The conversation is represented
    by the two characters involved in the conversation and a series of lines between
    those characters in the movie.

    The endpoint ensures that all characters are part of the referenced movie,
    that the characters are not the same, and that the lines of a conversation
    match the characters involved in the conversation.

    Line sort is set based on the order in which the lines are provided in the
    request body.

    The endpoint returns the id of the resulting conversation that was created.
    """

    # TODO: Remove the following two lines. This is just a placeholder to show
    # how you could implement persistent storage.

    # print(conversation)
    
    # db.logs.append({"post_call_time": datetime.now(), "movie_id_added_to": movie_id})
    # db.upload_new_log()
    
    # ensures the endpoint are part of the movie, chars are not the same, and lines match chars in convo
    if conversation.character_1_id == conversation.character_2_id:
        raise HTTPException(status_code=404, detail="conversation never existed.")

    char1_found = None
    char2_found = None
    for conversation_id in db.convos:
        convo = db.convos.get(conversation_id)
        if convo.movie_id == movie_id:
            if convo.c1_id == conversation.character_1_id:
                char1_found = True
            elif convo.c2_id == conversation.character_2_id:
                char2_found = True
            elif convo.c1_id == conversation.character_2_id:
                char2_found = True
            elif convo.c2_id == conversation.character_1_id:
                char1_found = True
            
            if char1_found == True and char2_found == True:
                break
    
    if char1_found != True or char2_found != True:
        raise HTTPException(status_code=404, detail="conversation never existed.")
    
    for line in conversation.lines:
        if line.character_id != conversation.character_1_id or line.character_id != conversation.character_2_id:
            raise HTTPException(status_code=404, detail="conversation never existed.")

    
    
    


    

 