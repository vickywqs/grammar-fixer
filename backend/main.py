from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, BaseSettings
from langdetect import detect
import openai
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str
    tone: str = "default"
    language: str = None

@app.post("/fix-grammar")
async def fix_grammar(data: TextRequest):
    language = data.language or detect(data.text)
    prompt = f"Correct grammar and rewrite this in a '{data.tone}' tone in {language}:
{data.text}"
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a multilingual grammar fixer and rewriter."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"corrected": res.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
