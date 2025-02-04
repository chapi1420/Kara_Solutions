# test_main.py
from fastapi.testclient import TestClient
from ..API.main import app

client = TestClient(app)

def test_create_message():
    response = client.post("/messages/", json={
        "channel_title": "Test Channel",
        "channel_username": "@testchannel",
        "message_id": 12345,
        "message": "This is a test message",
        "message_date": "2024-02-04T12:00:00",
        "media_path": "test/path",
        "emoji_used": "😊",
        "youtube_links": "https://youtube.com/test"
    })
    assert response.status_code == 200
    assert response.json()["message_id"] == 12345

def test_read_message():
    response = client.get("/messages/12345")
    assert response.status_code == 200
    assert response.json()["message_id"] == 12345

def test_list_messages():
    response = client.get("/messages/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_message():
    response = client.delete("/messages/12345")
    assert response.status_code == 200
