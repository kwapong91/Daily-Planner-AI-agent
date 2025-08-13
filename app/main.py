from fastapi import FastAPI
import requests

app = FastAPI(title="AI Planner")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}