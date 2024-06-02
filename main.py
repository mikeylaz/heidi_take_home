from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import Transcript
from api.v1.endpoints import voice_to_text

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client["voice_to_text_db"]

    # Initialize Beanie with the Transcript document
    await init_beanie(database, document_models=[Transcript])

app.include_router(voice_to_text.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)