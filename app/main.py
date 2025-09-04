# Use this command to run the server: fastapi dev main.py
from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Default to dev if ENV not set
env_file = f".env.{os.getenv('ENV', 'dev')}"
load_dotenv(env_file)

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
PORT = int(os.getenv("PORT", 8000))

app = FastAPI(title="AI Planner")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}