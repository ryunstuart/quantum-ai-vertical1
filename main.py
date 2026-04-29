from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from predict import predict_claim
from pydantic import BaseModel

app = FastAPI(title="Quantum Sentinel")

# Serve all files in the current directory as static
app.mount("/static", StaticFiles(directory="."), name="static")

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

@app.get("/quantum-shield.png")
async def serve_logo():
    return FileResponse("quantum-shield.png")

@app.post("/predict")
async def predict(claim: ClaimInput):
    return predict_claim(claim.dict())

@app.get("/health")
async def health():
    return {"status": "ok"}