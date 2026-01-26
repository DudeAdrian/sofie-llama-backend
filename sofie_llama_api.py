from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import your Llama Sofie model here
# from your_model_module import LlamaSofie

app = FastAPI()

# Allow CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize your model (replace with your actual model loading)
# sofie = LlamaSofie.load("path/to/model")

@app.post("/sofie/chat")
async def sofie_chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    context = data.get("context", [])
    # response = sofie.generate_response(user_message, context)
    response = "This is a placeholder response from Sofie."  # Replace with real model call
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)