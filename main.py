from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from pydantic import BaseModel ,computed_field,Field
from typing import Annotated, Literal

import json

app = FastAPI()

class Patient(BaseModel):

    id:Annotated[str,Field(..., description="id of the patient",examples=['p001'])]
    name:Annotated[str, Field(..., description="name of the patient",examples=['keerthan'])]
    city:Annotated[str,Field(..., description='name of the city')]
    age:Annotated[int,Field(...,gt=0,lt=100,description='age of the patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,description='gender of patient')]
    height:Annotated[float,Field(...,gt=0,description='height of the patient in meters')]
    weight:Annotated[float,Field(...,gt=0,description="weight of the patient in kgs")]


    @computed_field
    @property

    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property

    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'under wwight'
        elif self.bmi <25:
            return "good weight"
        elif self.bmi < 30 :
            return 'normal'
        else:
            return "obse weight" 


def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f)


@app.post('/create')
def create_patient(patient: Patient):


    #load existing data

    data =load_data()

    #checking the patient is already existed

    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient already exists' )
    
    #new patient data is added to database

    data[patient.id]=patient.model_dump(exclude=['id'])


    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient ceated sucessfully'})





