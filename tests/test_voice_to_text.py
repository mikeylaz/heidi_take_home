import os
import uuid
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from models import Transcript
import motor.motor_asyncio
from beanie import init_beanie
import pytest
from fastapi.testclient import TestClient
from main import app
import os
import uuid

@pytest.fixture(scope="module")
def client():
    # setup a test client for the FastAPI application, used for making test requests
    with TestClient(app) as c:
        yield c

def test_voice_to_text_valid_file(client):
    # test case to verify that a valid audio file returns a successful response
    with open("tests/test_audio.mp3", "rb") as audio:
        response = client.post("/api/v1/voice-to-text", files={"file": audio})
        assert response.status_code == 200
        response_data = response.json()
        assert "transcript_id" in response_data
        assert "content" in response_data

def test_voice_to_text_invalid_file_type(client):
    # test case to check handling of unsupported file types
    with open("tests/test_audio.txt", "rb") as audio:
        response = client.post("/api/v1/voice-to-text", files={"file": audio})
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["detail"] == "Invalid file type"

def test_database_insertion(client):
    # test case to check the database insertion of a transcript
    transcript_id = str(uuid.uuid4())
    test_transcript = {
        "audio_source": "test_source.mp3",
        "content": "This is a test transcript.",
        "status": "completed",
        "created_time": "2023-05-01T00:00:00",
        "updated_time": "2023-05-01T00:00:00",
    }
    transcript = Transcript(**test_transcript)
    transcript.id = transcript_id
    transcript.insert()

    # fetch the inserted transcript
    fetched_transcript = Transcript.find_one(Transcript.id == transcript_id)
    assert fetched_transcript is not None
    assert fetched_transcript.content == "This is a test transcript."