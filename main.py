from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import requests
import io

app = FastAPI()

#API key
ELEVENLABS_API_KEY = "sk_725a7a498d48d8e3da9fd616b122a81d0e49b8281fc29b80"


# Model cho request
class TextRequest(BaseModel):
    text: str
    voice_id: str = "nPczCjzI2devNBz1zQrb"


@app.post("/tts/")
async def text_to_speech(req: TextRequest):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{req.voice_id}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": req.text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        audio_data = io.BytesIO(response.content)
        return StreamingResponse(audio_data, media_type="audio/mpeg")
    else:
        return {"error": "Failed to generate audio", "status": response.status_code}

@app.get("/voices/")
def get_voices():
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
    return response.json()

