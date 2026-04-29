from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from predict import predict_claim
from pydantic import BaseModel
import os

app = FastAPI(title="Quantum Sentinel")

# Mount the root directory as static files
app.mount("/", StaticFiles(directory=".", html=True), name="static")

class ClaimInput(BaseModel):
    member_age: int
    billed_amount: float
    days_since_injury: int
    num_procedures: int
    procedure_cpt: str = "99214"
    diagnosis_icd: str = "M54.5"
    claim_type: str = "WorkersComp"

@app.post("/predict")
async def predict(claim: ClaimInput):
    return predict_claim(claim.dict())

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}