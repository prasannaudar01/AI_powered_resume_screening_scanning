import streamlit as st
import pandas as pd
import os
import base64
from processing import extract_text_from_pdf, rank_resumes, normalize_score

# Create a folder to store resumes
UPLOAD_FOLDER = "uploaded_resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to set background image
def set_background(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()

        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    else:
        st.warning("Background image not found!")

# Set background image
set_background("assets/pexels-goumbik-590041.jpg")

# Load custom CSS
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("CSS file not found!")

st.title("AI Resume Screening & Candidate Ranking System")

st.header("Job Description")
job_description = st.text_area("Enter the job description")

st.header("Upload Resumes")
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files and job_description.strip():
    st.header("Ranking Resumes")
    
    resume_texts = []
    file_names = []
    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())  # Save the file
        
        text = extract_text_from_pdf(file)
        resume_texts.append(text)
        file_names.append(file.name)
    
    scores = rank_resumes(job_description, resume_texts)
    normalized_scores = [normalize_score(score) for score in scores]
    
    results = pd.DataFrame({"Resume": file_names, "Score (%)": normalized_scores})
    results = results.sort_values(by="Score (%)", ascending=False)
    
    # Save rankings to a CSV file
    results.to_csv(os.path.join(UPLOAD_FOLDER, "resume_rankings.csv"), index=False)
    
    st.write(results)
    st.success("Resumes and rankings have been saved successfully!")
