from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from predict import predict_claim
from pydantic import BaseModel
from logger import get_monthly_summary

app = FastAPI(title="Quantum One AI Layer")

# Serve the nice dashboard at the root URL
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def serve_dashboard():
    return FileResponse("index.html")

# Updated Claim Input Model (with new fields)
class ClaimInput(BaseModel):
    member_age: int
    billed_amount: float
    days_since_injury: int
    num_procedures: int
    procedure_cpt: str
    diagnosis_icd: str
    claim_type: str
    # New fields (optional with defaults)
    provider_fraud_history: int = 0
    repeat_claimant: int = 0          # 0 = No, 1 = Yes
    provider_id: int = 123456

@app.post("/predict")
async def predict(claim: ClaimInput):
    return predict_claim(claim.dict())

# New Savings Report Endpoint
@app.get("/savings-report")
async def savings_report():
    return get_monthly_summary()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)