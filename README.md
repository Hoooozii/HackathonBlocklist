# HackathonBlocklist

Simple FastAPI service that returns a JSON blocklist based on a child's age and hobbies.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your key:

```
GEMINI_API_KEY=YOUR_KEY_HERE
```

Run the server:

```bash
uvicorn PromptAI:app --reload
```

Or using Make:

```bash
make run
```

## Test with curl

```bash
curl -X POST http://127.0.0.1:8000/recommendations \
  -H "Content-Type: application/json" \
  -d '{"age":10,"hobbies":["Minecraft","YouTube","Roblox"]}'
```

## Example response

```json
{
  "items": [
    {"type": "website", "name": "example-adult-site.com", "reason": "adult content", "confidence": 0.92},
    {"type": "app", "name": "SomeSocialApp", "reason": "general social media", "confidence": 0.81}
  ]
}
```

## Notes

- Edit `RULES` inside `PromptAI.py` to match your team's policy.
- Keep your API key on the server only.
