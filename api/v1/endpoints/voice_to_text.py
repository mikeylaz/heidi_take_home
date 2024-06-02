from fastapi import APIRouter, UploadFile, File, HTTPException
from models import Transcript
from services.voice_to_text_service import convert_voice_to_text
import os
import uuid

router = APIRouter()

@router.post("/voice-to-text")
async def voice_to_text(file: UploadFile = File(...)):
    # this is where we check the content type of the uploaded file 
    if file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Invalid file type")
    # generate a unique filename in a temporary directory to save the file
    file_location = f"temp/{uuid.uuid4()}.mp3"
    
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as audio_file:
        audio_file.write(file.file.read())

    # convert the audio file to text using the voice_to_text service
    transcript_content = await convert_voice_to_text(file_location)

    transcript = Transcript(
        audio_source=file_location,
        content=transcript_content,
        status="completed"
    )
    await transcript.insert() # insert into the database

    os.remove(file_location)  # clean up the temporary file

    return {"transcript_id": str(transcript.id), "content": transcript_content}