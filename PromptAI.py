# PromptAI.py
import json
import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env next to this file
DOTENV_PATH = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=DOTENV_PATH, override=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(f"Missing GEMINI_API_KEY. Check {DOTENV_PATH}")

app = FastAPI()
client = genai.Client(api_key=API_KEY)

# Edit these rules to match your team's policy.
RULES = """
Age 6-10: Block adult content, gambling, and general social media.
Age 11-13: Block adult content and gambling; allow kids versions where possible.
If hobby is Minecraft/Roblox: block scam, cheat, or unsafe mod sites.
If hobby is YouTube: block comments or adult content areas where possible.
""".strip()

class RecommendRequest(BaseModel):
    age: int
    hobbies: List[str]

def validate_response(data: dict) -> None:
    if not isinstance(data, dict):
        raise ValueError("Response is not an object")
    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("Response.items is not a list")

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Item is not an object")
        if item.get("type") not in {"website", "app"}:
            raise ValueError("Item.type must be 'website' or 'app'")
        if not isinstance(item.get("name"), str) or not item["name"].strip():
            raise ValueError("Item.name must be a non-empty string")
        if not isinstance(item.get("reason"), str) or not item["reason"].strip():
            raise ValueError("Item.reason must be a non-empty string")
        confidence = item.get("confidence")
        if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
            raise ValueError("Item.confidence must be between 0 and 1")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommendations")
def recommendations(req: RecommendRequest):
    prompt = (
        "You are a safety assistant for parents. "
        "Return ONLY valid JSON with this shape:\n"
        "{items:[{type:'website|app', name:'', reason:'', confidence:0-1}]}\n\n"
        "Policy rules:\n"
        f"{RULES}\n\n"
        f"Child age: {req.age}\n"
        f"Hobbies: {', '.join(req.hobbies)}\n"
        "Suggest SPECIFIC real websites and apps to block (not categories). "
        "Use real site domains or app names."
    )

    last_error = None
    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Gemini request failed: {exc}")

        raw = response.text or ""
        try:
            data = json.loads(raw)
            validate_response(data)
            return data
        except (json.JSONDecodeError, ValueError) as exc:
            last_error = exc

    raise HTTPException(status_code=500, detail=f"Model returned invalid JSON after retry: {last_error}")
