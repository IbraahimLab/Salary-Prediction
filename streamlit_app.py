import streamlit as st
import requests

st.title("Salary Prediction App")

# Input fields for user
Gender = st.selectbox("Gender", ["Male", "Female"])
Education_Level = st.selectbox("Education Level", ["Bachelor", "Master", "PhD"])
Job_Title = st.selectbox("Job Title", ["Data Scientist", "Software Engineer", "Product Manager", "Business Analyst", "HR Specialist"])
Age = st.number_input("Age", min_value=18, max_value=70, value=25)
Years_of_Experience = st.number_input("Years of Experience", min_value=0.0, max_value=50.0, value=1.0)

# Encode Gender (assuming 0 for Female, 1 for Male)
gender_encoded = 1 if Gender == "Male" else 0

if st.button("Predict Salary"):
    payload = {
        "Gender": gender_encoded,
        "Job_Title": Job_Title,
        "Education_Level": Education_Level,
        "Age": Age,
        "Years_of_Experience": Years_of_Experience
    }
    response = requests.post("http://localhost:8000/predict", json=payload)
    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Salary: {result['predicted_salary']}")
    else:
        st.error("Error: Could not get prediction from API.")
