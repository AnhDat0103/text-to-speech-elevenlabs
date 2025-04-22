from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from gtts import gTTS
import requests
import io
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

app = FastAPI()

class TextRequest(BaseModel):
    text: str
    voice_id: str = "IKne3meq5aSn9XLyUdCD"

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

@app.post("/format-code")
def format_code(req: TextRequest):
    def split_text_into_paragraphs(text: str, max_length: int = 500) -> list:
        # Initialize variables
        paragraphs = []
        current_paragraph = ""
        
        # Split text into sentences (assuming periods mark the end of sentences)
        sentences = text.split('.')
        
        for sentence in sentences:
            # Skip empty sentences
            if not sentence.strip():
                continue
                
            # Add period back to the sentence
            sentence = sentence.strip() + '.'
            
            # If adding this sentence would exceed max_length,
            # store current paragraph and start a new one
            if len(current_paragraph + sentence) > max_length:
                if current_paragraph:
                    paragraphs.append(current_paragraph.strip())
                current_paragraph = sentence
            else:
                # Add sentence to current paragraph
                current_paragraph = (current_paragraph + ' ' + sentence).strip()
        
        # Add the last paragraph if it's not empty
        if current_paragraph:
            paragraphs.append(current_paragraph.strip())
            
        return paragraphs

    # Process the input text
    formatted_paragraphs = split_text_into_paragraphs(req.text)
    
    # Return the formatted result
    return {"formatted_text": formatted_paragraphs}