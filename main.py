from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Quantum Sentinel")

# Serve static files (logo, etc.)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/quantum-shield.png")
async def shield():
    return FileResponse("quantum-shield.png")

@app.post("/predict")
async def predict(claim: dict):
    # Your existing predict logic here...
    pass  # (keep your current predict code)