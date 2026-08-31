import streamlit as st
import requests

# Ensure this matches your FastAPI port and path
API_URL = "http://localhost:8000/create"

st.title("PATIENT MANAGEMENT API")
st.markdown("### CREATE PATIENT")

# INPUT FIELDS (Updated to match Pydantic constraints)
patient_id = st.number_input("Patient ID", min_value=1, step=1)  # Added missing ID
name = st.text_input("Patient Name", value="John Doe")
age = st.number_input("Age", min_value=1, max_value=99, value=30)
height = st.number_input("Height (meters)", min_value=1, max_value=10, value=2)
city = st.text_input("City", value="New York")

# Fixed casing for "Non-Binary" to match your literal validator
gender = st.selectbox("Gender", ["Male", "Female", "Non-Binary"])

# Phone number input as text to match backend `str` type
phone_number = st.text_input("Phone Number", value="1234567890")
weight = st.number_input("Weight (kg)", min_value=1, max_value=500, value=70)

# SUBMIT BUTTON
if st.button("Register Patient"):
    # Package the payload exactly how the backend Patient model expects it
    payload = {
        "id": patient_id,
        "name": name,
        "city": city,
        "age": age,
        "gender": gender,
        "phone_number": phone_number,
        "weight": weight,
        "height": height
    }

    try:
        # Send a POST request to the API
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200 or response.status_code == 201:
            st.success("Patient created successfully!")
            st.json(response.json())  # Displays computed BMI and Verdict
        else:
            st.error(f"Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend server. Is Uvicorn running?")
