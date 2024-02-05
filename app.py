import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response= model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
        
    return text

input_promt="""
hey act like a skilled or very experience ATS(Application Tracking System) with a deep understanding
of tech fields, software engineering, data science, data analyst and big data engennier. Your task is to evaluate the resuem to given job descriprion
You must consider the job market is verify competitive and you should provide best assistance for improveing the resume. Assign the percentage Matching based on jd and the missing keywords with
high accuracy.
resume:{text}
description:{jd}

i want the responce in one single string having the structure {{"JD Match":"%", "Missing Key words:[]", "Profile Summary":"" }}
"""



##
st.title("Smart ATS")
st.text("Imporove your resume ATS")
jd=st.text_area("Paste Your JOb description")
uploaded_file=st.file_uploader("Upload Your Resume", type="pdf", help="Please upload your resume in pdf")
submit = st.button("submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_promt)
        st.subheader(response)