"""
S.O.F.I.E. Wellness Orchestration API (FastAPI)
----------------------------------------------
This API exposes the core S.O.F.I.E. orchestration logic for frontend (web/mobile) integration.
- Regulation before reasoning
- Consent before computation
- Enoughness over optimization
- Slow paths and silence are valid
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
from sofie_orchestrator import sofie_respond

app = FastAPI()

class CheckIn(BaseModel):
    message: str
    consent: bool = True
    chat_history: Optional[List[dict]] = None

@app.post("/check-in")
def check_in(data: CheckIn):
    if not data.consent:
        return {"response": "I’m here when you’re ready."}
    # Only respond if user is ready and consents
    reply = sofie_respond(data.message, data.chat_history or [])
    return {"response": reply}

# Optional: Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok", "sofie": "ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
