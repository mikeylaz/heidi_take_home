import requests
import time

# my assemblyAI information
ASSEMBLYAI_API_URL = "https://api.assemblyai.com/v2"
ASSEMBLYAI_API_KEY = "86ed9e6354b542408bf9eaa80e0b8b03"

async def upload_audio(file_path: str) -> str:
    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
    }
    with open(file_path, 'rb') as audio_file:
        #  post the audio file to the AssemblyAI API to get the URL for transcription
        response = requests.post(f"{ASSEMBLYAI_API_URL}/upload", headers=headers, files={"file": audio_file})

    response_data = response.json() 
    
    return response_data['upload_url'] # return the URL where the uploaded file is stored

async def transcribe_audio(audio_url: str) -> str:
    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }
    payload = {
        "audio_url": audio_url
    }
    response = requests.post(f"{ASSEMBLYAI_API_URL}/transcript", headers=headers, json=payload)
    response_data = response.json()
    transcript_id = response_data['id']

    # polling to get the transcription result
    while True:
        transcript_response = requests.get(f"{ASSEMBLYAI_API_URL}/transcript/{transcript_id}", headers=headers)
        transcript_data = transcript_response.json()

        if transcript_data['status'] == 'completed':
            return transcript_data['text']
        elif transcript_data['status'] == 'failed':
            raise Exception("Transcription failed")
        
        time.sleep(5)  #wait for 5 seconds before polling again

async def convert_voice_to_text(file_path: str) -> str:
    audio_url = await upload_audio(file_path)  # upload the audio file and get its URL
    transcript_text = await transcribe_audio(audio_url)  # transcribe the audio from the URL
    return transcript_text  # return the transcription result