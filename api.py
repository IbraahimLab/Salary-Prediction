from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# Load the trained model
model = joblib.load('salary_prediction_model.pkl')

app = FastAPI()

# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SalaryFeatures(BaseModel):
    Gender: int
    Job_Title: str
    Education_Level: str
    Age: int
    Years_of_Experience: float



# Ordinal encoding for Education Level
education_mapping = {"Bachelor": 0, "Master": 1, "PhD": 2}
# Example job title encoding
job_title_mapping = {
    "Data Scientist": 0,
    "Software Engineer": 1,
    "Product Manager": 2,
    "Business Analyst": 3,
    "HR Specialist": 4
}

@app.post("/predict")
async def predict_salary(features: SalaryFeatures):
    # Encode Education Level and Job Title
    education_encoded = education_mapping.get(features.Education_Level, 0)
    job_title_encoded = job_title_mapping.get(features.Job_Title, 0)
    input_data = np.array([[features.Gender, job_title_encoded, education_encoded, features.Age, features.Years_of_Experience]])
    prediction = model.predict(input_data)
    return {"predicted_salary": float(prediction[0])}
