from fastapi import FastAPI
from simulation import run_shadowcity

app = FastAPI(title="ShadowCity Multi-Agent AI")

@app.get("/")
def home():
    return {"message": "ShadowCity AI is running"}

@app.get("/simulate")
def simulate(steps: int = 20):
    result = run_shadowcity(steps)
    return result