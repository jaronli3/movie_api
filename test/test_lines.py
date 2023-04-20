from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_line():
    response = client.get("/lines/49")
    assert response.status_code == 200

    with open("test/lines/49.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_line1():
    response = client.get("/lines/64")
    assert response.status_code == 200

    with open("test/lines/64.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_lines_spoken_by_character1():
    response = client.get("/lines_spoken_by_character/?character_name=bianca&limit=50&offset=0")
    assert response.status_code == 200

    with open("test/lines/character-name=bianca&limit=50&offset=0.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_lines_spoken_by_character2():
    response = client.get("/lines_spoken_by_character/?character_name=leeloo&limit=250&offset=14")
    assert response.status_code == 200

    with open("test/lines/character-name=leeloo&limit=250&offset=14.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_lines1():
    response = client.get("/lines/?line_name=no&limit=50&offset=0&sort=line_text")
    assert response.status_code == 200

    with open("test/lines/line-name=no&limit=50&offset=0&sort=line_text.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_lines2():
    response = client.get("/lines/?line_name=believe&limit=250&offset=20&sort=movie")
    assert response.status_code == 200

    with open("test/lines/line-name=believe&limit=250&offset=20&sort=movie.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_lines3():
    response = client.get("/lines/?line_name=little&limit=20&offset=3&sort=character")
    assert response.status_code == 200

    with open("test/lines/line-name=little&limit=20&offset=3&sort=character.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_lines4():
    response = client.get("/lines/?line_name=attempt&limit=15&offset=10&sort=line_id")
    assert response.status_code == 200

    with open("test/lines/line-name=attempt&limit=15&offset=10&sort=line_id.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_404():
    response = client.get("/movies/1")
    assert response.status_code == 404