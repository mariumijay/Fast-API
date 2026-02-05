from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import os, json
from dotenv import load_dotenv
from typing import Annotated , Literal, List

load_dotenv() # load variables from .env file

app = FastAPI()

USERS = json.loads(os.getenv("USERS","{}")) # Load USERS from .env fie

def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data,f)

class Patient(BaseModel):
    patient_id: Annotated[str, Field(...,description="Username",examples=["1","2","3"])]
    first_name: Annotated[str, Field(..., description="Enter First Name")]
    last_name: Annotated[str, Field(..., description="Enter last Name")]
    age: Annotated[int, Field(..., ge=0 , le=120, description="Enter Age")]
    gender: Annotated[Literal["male","female","others"], Field(..., description="Enter Gender", examples=["male","female"])]
    blood_group: Annotated[Literal["A+","A-","B+","B-","AB+","AB-","O+","O-"], Field(..., description="Enter Blood Group",examples=["A+","B-"])]
    contact_number: Annotated[str, Field(..., description="Enter Contact Number")]
    email: Annotated[str, Field(...,description="Enter Email ID",examples=["xyz@gmail.com"])]
    address: Annotated[str, Field(..., description="Enter Address")]
    medical_history: Annotated[List, Field(..., description="Enter Medical History")]
    allergies: Annotated[List, Field(..., description="Enter Allergies")]
    current_medications: Annotated[List, Field(..., description="Enter Current Medications")]

@app.get("/")
def home():
    return{ 'message' : 'Welcome to FastAPI'}

@app.post("/predict")   # why showing length 6?
def predict(data: Patient):
    return {"patient ID Length" : len(data.patient_id),
            "email ID length" : len(data.email)
            } 

@app.post("/login/{user_id}/{password}")
def login(    
    user_id: Annotated[str, Path(...,description="Enter ID")],
    password: Annotated[str, Path(...,description="Enter Password")]
):                                                                      # Parameters are defined in the path and not in the request body
    if user_id not in USERS:
        raise HTTPException(status_code=404,detail="User not found")
    if USERS[user_id] != password:
        raise HTTPException(status_code=404,detail="Incorrect password")
    return{'message':f'Login Successful {user_id}'}

@app.post("/create")
def create_user(user: Patient):  # Parameters are defined in the request body and not in the path

    # load existing users
    data = load_data()

    # check if user already exists
    if user.patient_id in data:
        raise HTTPException(status_code=404, detail="User aleady exists")
    
    #new user creation 

     # convert Pydantic model to dictionary
    data[user.patient_id] = user.model_dump(exclude={"patient_id"})  # primary way to convert a Pydantic model instance into a Python dictionary
    
    # save to json file
    save_data(data)

    return JSONResponse(status_code=201, content={"message": f"User created successfully Patient ID: {user.patient_id} , Name : {user.first_name} {user.last_name}"})

    #return {"message" : f" User Created Successfully User _id : {user.patient_id}"}