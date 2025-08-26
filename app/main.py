# Use this command to run the server: fastapi dev main.py
from fastapi import FastAPI

app = FastAPI(title="AI Planner")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}