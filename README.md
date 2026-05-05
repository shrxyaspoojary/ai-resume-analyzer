# AI Resume Analyzer and Job Matcher

## Overview

This project is a simple web-based application that analyzes a candidate’s resume and compares it with a given job description. The goal is to provide a clear understanding of how well a resume aligns with job requirements by identifying matching skills, missing skills, and an overall similarity score.

It was developed as a practical way to explore basic natural language processing techniques and understand how text data can be compared using machine learning concepts.

---
## Application Preview

![Application Screenshot](screenshot.png)

## Features

* Upload a resume in PDF format
* Extract text from the resume
* Identify key skills from the resume
* Compare resume content with a job description
* Generate a match score based on similarity
* Highlight missing skills required for the job
* Provide simple suggestions for improvement
* Extract basic personal details such as name, email, and phone number

---

## How It Works

The application follows a straightforward pipeline:

1. The resume is uploaded and converted into raw text
2. The text is cleaned and processed
3. Skills are identified using keyword matching
4. Both resume and job description are converted into numerical vectors
5. Cosine similarity is used to calculate how closely they match
6. Missing skills are identified by comparing both sets

---

## Tech Stack

* Python
* Streamlit
* Scikit-learn
* PyPDF2

---

## Running the Project Locally

1. Clone the repository

   ```bash
   git clone https://github.com/your-username/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. Install dependencies

   ```bash
   pip install streamlit scikit-learn PyPDF2
   ```

3. Run the application

   ```bash
   python -m streamlit run app.py
   ```

---

## Limitations

* Skill extraction is based on predefined keywords
* Does not understand context or synonyms
* Accuracy depends on how the resume and job description are written

---

## Future Improvements

* Use TF-IDF or advanced NLP models for better matching
* Improve skill extraction using dynamic methods
* Add job recommendations based on resume content
* Enhance UI and reporting features

---

## Author

Shreyas S
