from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from predict import predict_claim
import uvicorn

app = FastAPI(title="Quantum Sentinel")

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

class ClaimInput(BaseModel):
    member_age: int
    billed_amount: float
    days_since_injury: int
    num_procedures: int
    procedure_cpt: str
    diagnosis_icd: str
    claim_type: str

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    return FileResponse("index.html")

@app.post("/predict")
async def predict(claim: ClaimInput):
    try:
        result = predict_claim(claim.dict())
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)