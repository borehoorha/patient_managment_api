import json
from models import Patient,Patient_Update
# from faker.providers.isbn import MAX_LENGTH
from fastapi.responses import JSONResponse
from fastapi import FastAPI,Path,Query,HTTPException
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to your specific streamlit domain
    allow_credentials=True,
    allow_methods=["*"], # Explicitly allows POST, OPTIONS, GET, etc.
    allow_headers=["*"],
)

# DUMMY
MODEL_VERSION = '1.1.0'

def patient_exists(patient_id: int, data) -> (int, bool):
    for i,patient in enumerate(data):
        if patient_id == patient['id']:
            return (i,True)
    return (None,False)


# JSON FILE HANDLING -------

def load_data():
    with open("./data/dummy_users.json", "r") as f:
    # with open("./data/file.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("./data/dummy_users.json","w") as f:
        json.dump(data,f)

# -------- END ---------

""" 
TITLE
DESCRIPTION
EXAMPLE
regex MAX_LENGHT MIN_LENGHT
"""
# ------- END POINTS ------- #
@app.get("/")
def home():
    return {"Hello":"This is Home"}

@app.get('/health')
def health():
    context ={
        "message":"OK",
        'version': MODEL_VERSION,
    }
    return JSONResponse(status_code=200, content=context)

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def patient(patient_id : int = Path(...,description="ID OF PATIENT",examples="123", MAX_LENGTH=100)):

    data = load_data()
    for patient in data:
        if patient_id == patient['id']:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")
    # return {"ERROR": "Patient not found"}


# ------- SORT ------
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Different on the basis of heigh and weight" ), order: str = Query("asc", description="Sort by ascending or descending")):
    valid_fields = ["weight","bmi","age"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail=f"Invalid sort order!")

    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(data,key = lambda x: x.get(sort_by, 0),reverse=sort_order)

    return sorted_data


# ------ CREATE -------
from fastapi import HTTPException
from fastapi.responses import JSONResponse


# Force FastAPI to listen for a POST method on this endpoint
@app.post('/create')
def create_patient(patient_: Patient):
    # Load existing data
    data = load_data()

    # Check if already exists:
    for patient in data:
        if patient_.id == patient['id']:
            raise HTTPException(status_code=400, detail="Patient already exists")

    # Use mode_dump() but include your @computed_field properties (bmi and verdict)
    patient_dict = patient_.model_dump()
    patient_dict['bmi'] = patient_.bmi
    patient_dict['verdict'] = patient_.verdict

    # Push/Dump data to json
    data.append(patient_dict)
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={"message": 'Patient created successfully!', "data": patient_dict}
    )


# ---- UPDATE ------
@app.put("/patient_edit/{patient_id}")
# def edit(patient_id: int,patient_: Patient):
def update_patient(patient_id: int, patient_update: Patient_Update):
    data = load_data()
    patient_exists = False
    existing_data = {}
    # check if already exists:
    for i, patient in enumerate(data):
        if patient_id == patient['id']:
            existing_data = patient
            patient_exists = True
            data.pop(i)
            break

    if patient_exists == False:
        raise HTTPException(status_code=400, detail="Patient Not Exists!!!")
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for k,v in updated_patient_info.items():
        existing_data[k] = v


    # existing_patient_info -> pydantic_object -> to clac bmi and verdict
    patient_pydantic_object = Patient(**existing_data)

    # ---> pydantic_object -> dict
    patient_pydantic_object.model_dump()

    # -> Add this dict to data
    data.append(existing_data)

    # -> Save data
    save_data(data)

    return JSONResponse(status_code=200, content={"message":'Patient updated successfully!'})


# ------ DELETE ------
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: int):
    data = load_data()
#   -- CHECK IF PATIENT EXISTS
    check = patient_exists(patient_id, data)
    if not check[1]:
        raise HTTPException(status_code=400, detail="Patient not exists")
    del data[check[0]]
    save_data(data)
    return JSONResponse(status_code=200, content={"message":'Patient deleted successfully!'})



# MY METHOD NOT IN TUTORIAL
@app.get("/patients/{search_term}")
def patient_search(search_term):
    search_term = search_term.strip().lower()
    data = load_data()
    l = list()
    for patient_ in data:
        if search_term in (patient_['name']).lower():
           l.append(patient_)
            # return patient_
    return (x for x in l)