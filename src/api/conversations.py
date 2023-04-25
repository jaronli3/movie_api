from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
from typing import List
from datetime import datetime
# from supabase import Client, create_client

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
        raise HTTPException(status_code=400, detail="character talking to themselves.")

    char1_found = None
    char2_found = None
    for conversation_id in db.conversations:
        convo = db.conversations.get(conversation_id)
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
        raise HTTPException(status_code=400, detail="both characters not in conversation.")
    
    for line in conversation.lines:
        if line.character_id != conversation.character_1_id and line.character_id != conversation.character_2_id:
            raise HTTPException(status_code=400, detail="conversation never existed.")


    movie_convo_log = db.read_new_logs()
    movie_convo_log_dict = {"post_call_time": datetime.now(), "movie_id_added_to": movie_id}
    movie_convo_log.append(movie_convo_log_dict)
    current_convo_id = list(db.conversations)[-1]
    updated_convo_id = int(current_convo_id) + 1

    conversation_lst = db.read_new_convos()

    conversation_dict = {"conversation_id": str(updated_convo_id),
                        "character1_id": conversation.character_1_id, 
                        "character2_id": conversation.character_2_id,
                        "movie_id": movie_id}

    conversation_lst.append(conversation_dict)

    line_lst = db.read_new_lines()
    line_sort_num = 1
    current_line_id = list(db.lines)[-1]
    updated_line_id = int(current_line_id) + 1
    for line in conversation.lines:
        new_line = {}
        new_line["line_id"] = updated_line_id
        new_line["character_id"] = line.character_id
        new_line["movie_id"] = movie_id
        new_line["conversation_id"] = conversation_dict["conversation_id"]
        new_line["line_sort"] = line_sort_num
        new_line["line_text"] = line.line_text
        line_lst.append(new_line)
        line_sort_num += 1
        updated_line_id += 1

    db.upload_new_log(movie_convo_log)
    db.upload_new_conversations(conversation_lst)
   
    db.upload_new_lines(line_lst)

    return str(updated_convo_id)