## TO DEVELOP API FOR DOCTOR'S APPOINTMENT APP
### API ENDPOINTS: 
- ####  create/
- #### view/
- #### view/{patient_id}/
- #### update/{patient_id}
- #### delete /{patient_id}
---
# IMPORTANT TERMS AND FUNC 
- ### Query parametes <?> : used for filtering,sorting,searching pagination without  <b> ALTERING ENDPOINT ITSELF </b>
- ### path() - used for documentation and showing metadata, hints for path parameters for your API endpoints.
- ### field_validator - default mode is < before:before conversion>
: - Used as a decorator
: - @field_validotr("variable_name")
: - Then define a function by parametes(cls<class>, value<value:variable value>)
- # patient_managment_api
