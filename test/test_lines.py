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

# def test_get_char_line():
#     response = client.get("/lines/")
#     assert response.status_code == 200

#     with open("test/lines/get_char_lines1.json", encoding="utf-8") as f:
#         assert response.json() == json.load(f)

def test_404():
    response = client.get("/movies/1")
    assert response.status_code == 404