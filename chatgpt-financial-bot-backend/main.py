from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

import openai
import os
import json
import requests
import uuid

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_KEY")
# openai.organization = os.getenv("OPEN_AI_ORG")
elevenlabs_key = os.getenv("ELEVENLABS_KEY")

app = FastAPI()

origins = [
    "http://localhost:5174",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/talk")
async def post_audio(file: UploadFile):
    user_message = transcribe_audio(file)
    chat_response = get_chat_response(user_message)
    audio_path = text_to_speech(chat_response)

    # Return the saved audio file as a downloadable response
    return FileResponse(
        path=audio_path,
        media_type="audio/mpeg",
        filename="output.mp3"
    )

@app.get("/clear")
async def clear_history():
    file = 'database.json'
    open(file, 'w').close()
    return {"message": "Chat history has been cleared"}

# ------------------- Helper Functions -----------------------

def transcribe_audio(file):
    with open(file.filename, 'wb') as buffer:
        buffer.write(file.file.read())
    with open(file.filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)
    return transcript

def get_chat_response(user_message):
    messages = load_messages()
    messages.append({"role": "user", "content": user_message['text']})

    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    parsed_gpt_response = gpt_response['choices'][0]['message']['content']
    save_messages(user_message['text'], parsed_gpt_response)
    return parsed_gpt_response

def load_messages():
    messages = []
    file = 'database.json'
    empty = not os.path.exists(file) or os.stat(file).st_size == 0

    if not empty:
        with open(file) as db_file:
            data = json.load(db_file)
            for item in data:
                messages.append(item)
    else:
        messages.append(
            {
                "role": "system",
                "content": "You are Finny, a friendly and witty financial assistant bot helping the user manage their personal and business finances. Ask short, smart questions to understand their spending, income, or goals. Keep responses helpful, under 30 words, and occasionally add a friendly joke or pun."
            }

        )
    return messages

def save_messages(user_message, gpt_response):
    file = 'database.json'
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response})
    with open(file, 'w') as f:
        json.dump(messages, f)

def text_to_speech(text):
    voice_id = 'pNInz6obpgDQGcFmaJgB'

    body = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }

    headers = {
        "Content-Type": "application/json",
        "accept": "audio/mpeg",
        "xi-api-key": elevenlabs_key
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    try:
        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            # Save audio content to unique file
            filename = f"response_{uuid.uuid4()}.mp3"
            filepath = os.path.join("audio", filename)
            os.makedirs("audio", exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(response.content)
            return filepath
        else:
            print("Something went wrong:", response.text)
            return None
    except Exception as e:
        print("Error:", e)
        return None
