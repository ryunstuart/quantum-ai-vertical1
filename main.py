from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from predict import predict_claim
from pydantic import BaseModel
import os

app = FastAPI(title="Quantum Sentinel")

class ClaimInput(BaseModel):
    member_age: int
    billed_amount: float
    days_since_injury: int
    num_procedures: int
    procedure_cpt: str = "99214"
    diagnosis_icd: str = "M54.5"
    claim_type: str = "WorkersComp"

@app.get("/")
async def serve_dashboard():
    return FileResponse("index.html")

@app.post("/predict")
async def predict(claim: ClaimInput):
    try:
        return predict_claim(claim.dict())
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Simple static file serving
@app.get("/quantum-shield.png")
async def serve_logo():
    if os.path.exists("quantum-shield.png"):
        return FileResponse("quantum-shield.png")
    return {"error": "Logo not found"}

@app.get("/health")
async def health():
    return {"status": "ok"}