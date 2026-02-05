from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated , Literal, List, Optional
import json
from fastapi.responses import JSONResponse

app = FastAPI()

class PatientUpdate(BaseModel):
    first_name: Annotated[Optional[str], Field(default=None,description="Enter First Name")]
    last_name: Annotated[Optional[str], Field(default=None,description="Enter last Name")]
    age: Annotated[Optional[int], Field(default=None,ge=0 , le=120, description="Enter Age")]
    gender: Annotated[Optional[Literal["male","female","others"]], Field(default=None,description="Enter Gender", examples=["male","female"])]
    blood_group: Annotated[Optional[Literal["A+","A-","B+","B-","AB+","AB-","O+","O-"]], Field(default=None,description="Enter Blood Group",examples=["A+","B-"])]
    contact_number: Annotated[Optional[str], Field(default=None,description="Enter Contact Number")]
    email: Annotated[Optional[str], Field(default=None,description="Enter Email ID",examples=["xyz@gmail.com"])]
    address: Annotated[Optional[str], Field(default=None,description="Enter Address")]
    medical_history: Annotated[Optional[List[str]], Field(default=None,description="Enter Medical History")]
    allergies: Annotated[Optional[List[str]], Field(default=None,description="Enter Allergies")]
    current_medications: Annotated[Optional[List[str]], Field(default=None,description="Enter Current Medications")]

def load_data():
    with open("data.json","r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("data.json", "w")as f:
        json.dump(data,f)
        

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):

    #Load existing data
    data = load_data()

    #check if patient_id exists in existing data
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    #extract existing patient data
    current_patient_data = data[patient_id]

    #convert pydantic model ( PatientUpdate) to dictionary with exlude_unset=True
    updated_patient_data = patient_update.model_dump(exclude_unset=True)

    #update existing patient data with new data
    current_patient_data.update(updated_patient_data)

    #save updated data back to file
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient data updated successfully", "patient_id": patient_id})

    