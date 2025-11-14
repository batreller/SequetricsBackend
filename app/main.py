from fastapi import FastAPI
from app.api import auth, voice, history

app = FastAPI(title="Voice to Text API")

app.include_router(auth.router, tags=["Authentication"])
app.include_router(voice.router, tags=["Voice Processing"])
app.include_router(history.router, tags=["History"])


@app.get("/")
async def root():
    return {"message": "Voice to Text API"}
