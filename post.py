from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel
import os, json
from dotenv import load_dotenv
from typing import Annotated

load_dotenv() # load variables from .env file

app = FastAPI()

USERS = json.loads(os.getenv("USERS","{}")) # Load USERS from .env fie

@app.get("/")
def home():
    return{ 'message' : 'Welcome to FastAPI'}

@app.post("/login/{user_id}/{password}")
def login(
    user_id: Annotated[str, Path(...,description="Enter ID")],
    password: Annotated[str, Path(...,description="Enter Password")]
):
    if user_id not in USERS:
        raise HTTPException(status_code=404,detail="User not found")
    if USERS[user_id] != password:
        raise HTTPException(status_code=404,detail="Incorrect password")
    return{'message':'Login Successful'}