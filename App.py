import streamlit as st
import pandas as pd
from processing import extract_text_from_pdf, rank_resumes, normalize_score
import base64
import os

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

# Set background image (Update path if needed)
set_background("assets/pexels-goumbik-590041.jpg")

# Load custom CSS safely
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("CSS file not found!")

# Streamlit App Title
st.title("AI Resume Screening & Candidate Ranking System")

# Job Description Input
st.header("Job Description")
job_description = st.text_area("Enter the job description")

# Resume Upload
st.header("Upload Resumes")
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

# Process uploaded resumes
if uploaded_files and job_description.strip():
    st.header("Ranking Resumes")
    
    resumes = [extract_text_from_pdf(file) for file in uploaded_files]
    scores = rank_resumes(job_description, resumes)

    # Convert scores to percentage
    normalized_scores = [normalize_score(score) for score in scores]

    # Display results
    results = pd.DataFrame({"Resume": [file.name for file in uploaded_files], "Score (%)": normalized_scores})
    results = results.sort_values(by="Score (%)", ascending=False)

    st.write(results)
