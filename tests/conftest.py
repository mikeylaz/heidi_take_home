import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from main import app
from models import Transcript

@pytest.fixture(scope="module")
async def test_app():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    test_db = client["voice_to_text_test_db"]

    await init_beanie(database=test_db, document_models=[Transcript])

    yield TestClient(app)

    # drop the test database after the tests
    client.drop_database("voice_to_text_test_db")