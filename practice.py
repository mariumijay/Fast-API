from fastapi import FastAPI , Path , HTTPException , Query
import json
from pydantic import BaseModel , Field 
from typing import Annotated , Literal

app = FastAPI()

class Patient(BaseModel):
    patient_id: str
    age: int

@app.post('/predict')
def predict(data: Patient):
    return{"length": len(data.patient_id)}

def load_data():
    with open('data.json','r') as f:
        data = json.load(f)
    return data

@app.get("/")
def predict():
    return{"msg" : "PATIENT MANAGMENT API"}

@app.get('/about')
def about():
    return{'about' : 'API manages patient data and provides health predictions.'}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='The ID of the Patient to retrieve')):
    # load all the data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    #else:
    #   return {'error' : 'Patient ID not Found' }
    raise HTTPException(status_code=404, detail='Patient ID not found')
    
@app.get('/sort')
def sorted_data( sort_by: str = Query(...,description='Field to sort the data by')):
    data = load_data()

    if sort_by not in ["age","patient_id"]:
        raise HTTPException(status_code=404,detail="Not a valid field to sort by")
    
    sort_order = True if sort_by == "age" else False
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0),reverse=sort_order)

    return sorted_data
