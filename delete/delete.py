from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import json

app = FastAPI()

def load_data():
    with open("data.json","r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("data.json","w") as f:
        json.dump(data,f)

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):

    #Load Data
    data = load_data()

    #check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
     
    #delete patient
    del data[patient_id]

    #save data
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})
