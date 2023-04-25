from fastapi.testclient import TestClient
from src import database as db
from src.api.server import app

import json

client = TestClient(app)

def test_add_convo1():
    convo =  {
    "character_1_id": 168,
    "character_2_id": 174,
    "lines": [
        {
        "character_id": 168,
        "line_text": "my name is not jaron."
        },
        {
        "character_id": 174,
        "line_text": "oh i thought it was?"
        }
        ]
    }
    
    response = client.post("/movies/11/conversations/", json=convo)

    assert response.status_code == 200

def test_convo1():
    found = False
    for line_id in db.lines:
        line = db.lines.get(line_id)
        if line.line_text == "my name is not jaron.":
            found = True
    
    assert found == True
    