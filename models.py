from pydantic import BaseModel,Field,computed_field,field_validator
from typing import List,Annotated,Dict,Literal,Optional

class Patient(BaseModel):
    id: Annotated[int, Field(...,description="ID of the Patient",examples=[1,2,3])]
    name: Annotated[str,Field(description="Name of the Patient" )]
    city: Annotated[str,Field(description="City of the Patient")]
    age: Annotated[int,Field(description="Age of the Patient",gt=0,lt=100)]
    gender: Annotated[Literal['Male','Female','Non-Binary'],Field(description="Gender of the Patient")]
    phone_number: Annotated[str,Field(description="Phone Number of the Patient")]
    weight: Annotated[int,Field(description="Weight of the Patient in kgs",gt=0,)]
    height: Annotated[int,Field(description="Height of the Patient in m",gt=0,)]
    # bmi: Annotated[int,Field(description="BMI of the Patient")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi =  round(float(self.weight) / float(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        if self.bmi < 25:
            return "Normal"
        if self.bmi < 30:
            return "Overweight"
        if self.bmi < 35:
            return "Obedient"
        else:
            return "Obese"

# NEW MODEL FOR UPDATING
# WHERE ALL FIELDS WILL BE OPTIONAL
class Patient_Update(BaseModel):
    name: Annotated[Optional[str], Field(description="Name of the Patient",default=None)]
    city: Annotated[Optional[str], Field(description="City of the Patient",default=None)]
    age: Annotated[Optional[int], Field(description="Age of the Patient", gt=0, lt=100,default=None)]
    gender: Annotated[Optional[Literal['Male', 'Female', 'Non-Binary']], Field(description="Gender of the Patient",default=None)]
    phone_number: Annotated[Optional[str], Field(description="Phone Number of the Patient",default=None)]
    weight: Annotated[Optional[int], Field(description="Weight of the Patient in kgs", gt=0,default=None)]
    height: Annotated[Optional[int], Field(description="Height of the Patient in m", gt=0,default=None )]