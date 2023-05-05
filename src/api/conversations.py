from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
from typing import List
from datetime import datetime
# from supabase import Client, create_client

# FastAPI is inferring what the request body should look like
# based on the following two classes.

import sqlalchemy
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
    
    #EDGE CASES: One case where my code won't work in is if there are multiple calls made at the 
    #same time as data could potentially get overwritten or lost. Something to consider 
    # as well is the speed of the service if multiple calls are made at the same time and how to best 
    #optimize it to ensure the service is not slow and also for the service to not crash due to multiple
    #simultaneous calls. One thing I also couldn't figure out was once a conversation was added, the 
    #service was still reading from the original database and didn't take the new conversations and lines
    #into account.

    if conversation.character_1_id == conversation.character_2_id:
        raise HTTPException(status_code=400, detail="character talking to themselves.")

    for line in conversation.lines:
        if line.character_id != conversation.character_1_id and line.character_id != conversation.character_2_id:
            raise HTTPException(status_code=400, detail="conversation never existed.")
    
    stmt = sqlalchemy.select(db.chars.c.character_id, db.chars.c.movie_id).where((db.chars.c.character_id == conversation.character_1_id) |
                                                           (db.chars.c.character_id == conversation.character_2_id))

    with db.engine.connect() as conn:
        counter = 0
        result = conn.execute(stmt).fetchall()
        movie_id = None
        for x in result:
            if movie_id is None:
                movie_id = x.movie_id
            counter += 1
        if counter != 2:
            raise HTTPException(status_code=400, detail="both characters not in conversation.")
        
        stmt1 = sqlalchemy.select(db.convos.c.conversation_id).order_by(sqlalchemy.desc(db.convos.c.conversation_id))
        res = conn.execute(stmt1).fetchone()
        next_convo_id = res.conversation_id + 1
  

        conversation_dict = {"conversation_id": next_convo_id,
                            "character1_id": conversation.character_1_id, 
                            "character2_id": conversation.character_2_id,
                            "movie_id":  movie_id}

    
        line_sort_num = 1
        stmt2 = sqlalchemy.select(db.lines.c.line_id).order_by(sqlalchemy.desc(db.lines.c.line_id))
        res1 = conn.execute(stmt2).fetchone()
        next_line_id = res1.line_id + 1

        for line in conversation.lines:
            new_line = {}
            new_line["line_id"] = next_line_id
            new_line["character_id"] = line.character_id
            new_line["movie_id"] = movie_id
            new_line["conversation_id"] = next_convo_id
            new_line["line_sort"] = line_sort_num
            new_line["line_text"] = line.line_text
            line_sort_num += 1
            next_line_id += 1
            conn.execute(db.lines.insert().values(new_line))

        conn.execute(db.convos.insert().values(conversation_dict))
   
        conn.commit()

    return str(next_convo_id)