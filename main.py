from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from predict import predict_claim

app = FastAPI()

@app.get("/")
async def home():
    return FileResponse("index.html")

class Claim(BaseModel):
    member_age: int
    billed_amount: float
    days_since_injury: int
    num_procedures: int
    procedure_cpt: str
    diagnosis_icd: str
    claim_type: str

@app.post("/predict")
async def predict(claim: Claim):
    try:
        result = predict_claim(claim.dict())
        return result
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)