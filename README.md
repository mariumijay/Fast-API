# FastAPI CRUD Practice Project

A **FastAPI practice project** demonstrating modular CRUD operations (`GET`, `POST`, `PUT`, `DELETE`) with **Pydantic** data validation, **HTTPException** error handling, and clean project organization for a **Patient Management System**.

---

## 📂 Project Structure
```
FAST API/
│
├── get/                    # GET operations module
│   └── get.py
├── post/                   # POST operations module
│   └── post.py
├── put/                    # PUT operations module
│   └── put.py
├── delete/                 # DELETE operations module
│   └── delete.py
├── data.json               # JSON-based patient data storage
├── .env                    # Environment variables (user credentials)
├── main.py                 # FastAPI application entry point
└── README.md
```

---

## 🛠 Technologies Used

- **Python 3.11+**
- **FastAPI** – Modern web framework for building APIs
- **Pydantic** – Data validation using Python type annotations
- **Uvicorn** – Lightning-fast ASGI server
- **HTTPException** – Proper HTTP error handling
- **JSON** – Lightweight data persistence
- **python-dotenv** – Environment variable management

---

## ✨ Features

- ✅ **POST** – Create new patient records with automatic validation
- ✅ **GET** – Retrieve records using path and query parameters
- ✅ **PUT** – Update existing records (partial or full updates)
- ✅ **DELETE** – Safely remove records with error handling
- ✅ **Authentication** – User login system with credentials
- ✅ **Modular Architecture** – Each HTTP method in its own module
- ✅ **Data Validation** – Pydantic BaseModels ensure data integrity
- ✅ **Error Handling** – HTTPException for meaningful error responses
- ✅ **Sorting & Filtering** – Query parameters for data manipulation

---

## 📝 Pydantic Models

### Patient Model (Full)
```python
from pydantic import BaseModel, Field
from typing import Annotated, Literal, List

class Patient(BaseModel):
    patient_id: Annotated[str, Field(..., description="Username", examples=["1","2","3"])]
    first_name: Annotated[str, Field(..., description="Enter First Name")]
    last_name: Annotated[str, Field(..., description="Enter last Name")]
    age: Annotated[int, Field(..., ge=0, le=120, description="Enter Age")]
    gender: Annotated[Literal["male","female","others"], Field(..., description="Enter Gender")]
    blood_group: Annotated[Literal["A+","A-","B+","B-","AB+","AB-","O+","O-"], Field(...)]
    contact_number: Annotated[str, Field(..., description="Enter Contact Number")]
    email: Annotated[str, Field(..., description="Enter Email ID", examples=["xyz@gmail.com"])]
    address: Annotated[str, Field(..., description="Enter Address")]
    medical_history: Annotated[List, Field(..., description="Enter Medical History")]
    allergies: Annotated[List, Field(..., description="Enter Allergies")]
    current_medications: Annotated[List, Field(..., description="Enter Current Medications")]
```

### PatientUpdate Model (Partial Updates)
```python
from typing import Optional

class PatientUpdate(BaseModel):
    first_name: Annotated[Optional[str], Field(default=None, description="Enter First Name")]
    last_name: Annotated[Optional[str], Field(default=None, description="Enter last Name")]
    age: Annotated[Optional[int], Field(default=None, ge=0, le=120, description="Enter Age")]
    gender: Annotated[Optional[Literal["male","female","others"]], Field(default=None)]
    blood_group: Annotated[Optional[Literal["A+","A-","B+","B-","AB+","AB-","O+","O-"]], Field(default=None)]
    contact_number: Annotated[Optional[str], Field(default=None)]
    email: Annotated[Optional[str], Field(default=None)]
    address: Annotated[Optional[str], Field(default=None)]
    medical_history: Annotated[Optional[List[str]], Field(default=None)]
    allergies: Annotated[Optional[List[str]], Field(default=None)]
    current_medications: Annotated[Optional[List[str]], Field(default=None)]
```

---

## 🔌 API Endpoints

### **POST Operations** (`post/post.py`)

#### 1. Home Endpoint
```http
GET /
```
Returns a welcome message.

#### 2. Predict Endpoint (Test)
```http
POST /predict
```
**Request Body:**
```json
{
  "patient_id": "12345",
  "age": 30
}
```
**Response:**
```json
{
  "patient ID Length": 5,
  "email ID length": 15
}
```

#### 3. User Login
```http
POST /login/{user_id}/{password}
```
- **Authentication**: Validates credentials from `.env` file
- **Error Handling**: 
  - `404` if user not found
  - `404` if password incorrect

**Example:**
```http
POST /login/admin/password123
```

#### 4. Create Patient
```http
POST /create
```
**Request Body:**
```json
{
  "patient_id": "P001",
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "gender": "male",
  "blood_group": "O+",
  "contact_number": "+1234567890",
  "email": "john.doe@example.com",
  "address": "123 Main St",
  "medical_history": ["Diabetes"],
  "allergies": ["Peanuts"],
  "current_medications": ["Metformin"]
}
```
**Response:**
```json
{
  "message": "User created successfully Patient ID: P001, Name: John Doe"
}
```

---

### **GET Operations** (`get/get.py`)

#### 1. View All Patients
```http
GET /view
```
Returns all patient records from `data.json`.

#### 2. View Specific Patient
```http
GET /patient/{patient_id}
```
**Example:**
```http
GET /patient/P001
```
**Error**: `404` if patient not found

#### 3. Sort Patients
```http
GET /sort?sort_by=age
```
**Query Parameters:**
- `sort_by`: Field to sort by (`age` or `patient_id`)

**Example:**
```http
GET /sort?sort_by=age
```
**Response:** Returns patients sorted by age (descending)

---

### **PUT Operations** (`put/put.py`)

#### Update Patient
```http
PUT /edit/{patient_id}
```
**Supports partial updates** - only send fields you want to update.

**Request Body (Partial Update):**
```json
{
  "age": 31,
  "contact_number": "+9876543210",
  "email": "newemail@example.com"
}
```

**Response:**
```json
{
  "message": "Patient data updated successfully",
  "patient_id": "P001"
}
```

**Key Feature**: Uses `model_dump(exclude_unset=True)` to only update provided fields.

---

### **DELETE Operations** (`delete/delete.py`)

#### Delete Patient
```http
DELETE /delete/{patient_id}
```
**Example:**
```http
DELETE /delete/P001
```

**Response:**
```json
{
  "message": "Patient deleted successfully"
}
```

**Error**: `404` if patient not found

---

## 🚀 How to Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/Fast-API.git
cd "FAST API"
```

### 2️⃣ Create `.env` File
Create a `.env` file in the root directory:
```env
USERS={"admin":"password123","user1":"pass456"}
```

### 3️⃣ Install Dependencies
```bash
pip install fastapi uvicorn python-dotenv
```

### 4️⃣ Create `data.json`
Create an empty `data.json` file:
```json
{}
```

### 5️⃣ Start the Development Server
```bash
uvicorn main:app --reload
```

### 6️⃣ Access Interactive API Documentation
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📚 Key Implementation Details

### Data Persistence
```python
def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)
```

### Partial Update Logic (PUT)
```python
# Load existing patient data
current_patient_data = data[patient_id]

# Convert Pydantic model to dict (only set fields)
updated_patient_data = patient_update.model_dump(exclude_unset=True)

# Merge updates with existing data
current_patient_data.update(updated_patient_data)
```

### Error Handling Pattern
```python
if patient_id not in data:
    raise HTTPException(status_code=404, detail="Patient not found")
```

---

## 🎯 Learning Outcomes

This project demonstrates:
- ✅ **Modular FastAPI architecture** with separate files for each CRUD operation
- ✅ **Pydantic validation** with `Field()` constraints and `Annotated` types
- ✅ **Path parameters** (`/patient/{patient_id}`)
- ✅ **Query parameters** (`/sort?sort_by=age`)
- ✅ **Request body validation** with Pydantic models
- ✅ **Partial updates** using `model_dump(exclude_unset=True)`
- ✅ **HTTPException** for proper error handling
- ✅ **Environment variables** with `python-dotenv`
- ✅ **JSON file operations** for data persistence

---

## 🔮 Future Improvements

- [ ] Replace JSON with SQLite/PostgreSQL database
- [ ] Add JWT authentication instead of simple login
- [ ] Implement async I/O (`async def`)
- [ ] Add pagination for large datasets
- [ ] Add input sanitization and security measures
- [ ] Implement comprehensive test suite (pytest)
- [ ] Add Docker containerization
- [ ] Create frontend UI (React/Vue)
- [ ] Add API rate limiting
- [ ] Implement logging and monitoring

---

## 📄 File Structure Details

### `post/post.py` - POST Operations
- Patient registration
- User login
- Data validation

### `get/get.py` - GET Operations  
- Retrieve all patients
- Get specific patient by ID
- Sort and filter patients

### `put/put.py` - PUT Operations
- Update patient records
- Partial update support

### `delete/delete.py` - DELETE Operations
- Remove patient records
- Validation before deletion

---

## 🐛 Common Issues & Solutions

### Issue: `ModuleNotFoundError: No module named 'dotenv'`
**Solution:**
```bash
pip install python-dotenv
```

### Issue: `FileNotFoundError: data.json`
**Solution:** Create an empty `data.json` file:
```bash
echo "{}" > data.json
```

### Issue: `422 Unprocessable Entity`
**Solution:** Ensure all required fields are provided in request body

---

## 👤 Author

**Marium Ijaz**  
GitHub: [@mariumijay](https://github.com/mariumijay)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check the [issues page](https://github.com/mariumijay/Fast-API/issues).

---

**⭐ If you found this project helpful, please give it a star!**
