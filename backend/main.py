
import os
import uuid
import traceback

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from google.genai import types


# Get project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load API key from .env file
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")


# Create Gemini client
client = None

if API_KEY:
    client = genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(timeout=60000)
    )


# Create FastAPI application
app = FastAPI(
    title="AI Study Assistant",
    description="An AI-powered study assistant with conversation memory",
    version="1.0.0"
)


# Frontend directory
FRONTEND_DIR = BASE_DIR / "frontend"

# Serve frontend CSS and JavaScript files
app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)


# Store conversation history
conversations = {}


# Custom system prompt
SYSTEM_PROMPT = """
You are an AI Study Assistant.

Your role is to help students understand academic concepts.

Instructions:
1. Explain concepts in simple and clear language.
2. Give examples wherever necessary.
3. Use step-by-step explanations for difficult topics.
4. Be friendly, patient and supportive.
5. Help students prepare for examinations.
6. Keep answers organized and easy to understand.
"""


# Request model
class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


# Home endpoint
@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):

    # Check API key
    if not API_KEY or client is None:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is missing. Check your .env file."
        )

    # Validate message
    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    # Create or reuse conversation ID
    conversation_id = request.conversation_id

    if not conversation_id:
        conversation_id = str(uuid.uuid4())

    # Create conversation if it does not exist
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    # Get conversation history
    history = conversations[conversation_id]

    # Keep only the latest 10 messages
    recent_history = history[-10:]

    # Convert history into Gemini format
    contents = []

    for item in recent_history:
        contents.append(
            types.Content(
                role=item["role"],
                parts=[
                    types.Part.from_text(text=item["content"])
                ]
            )
        )

    # Add current user message
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_message)
            ]
        )
    )

    try:
        # Send request to Gemini
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )

        # Get AI response
        ai_response = response.text

        if not ai_response:
            raise ValueError("Gemini returned an empty response.")

        # Save messages only after successful response
        history.append({
            "role": "user",
            "content": user_message
        })

        history.append({
            "role": "model",
            "content": ai_response
        })

        return {
            "conversation_id": conversation_id,
            "response": ai_response
        }

    except Exception as error:

        print("\n========== GEMINI API ERROR ==========")
        print("ERROR TYPE:", type(error))
        print("ERROR MESSAGE:", str(error))
        traceback.print_exc()
        print("======================================\n")

        raise HTTPException(
            status_code=502,
            detail="Gemini API request failed. Check the server terminal."
        )
