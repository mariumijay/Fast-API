from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()
 

class Input(BaseModel):
    text: str
    temperature: float

@app.post("/predict")
def predict(data: Input):
    return {"length": len(data.text)}
