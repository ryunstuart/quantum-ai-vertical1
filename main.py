from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict_claim

app = FastAPI(title="Quantum One AI Layer")

class ClaimInput(BaseModel):
    member_age: int
    billed_amount: float
    days_since_injury: int
    num_procedures: int
    procedure_cpt: str
    diagnosis_icd: str
    claim_type: str
    provider_id: int = 123456   # optional

@app.post("/predict")
async def predict(claim: ClaimInput):
    result = predict_claim(claim.dict())
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)