import io
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from dotenv import load_dotenv

# LangChain components
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Load environment variables from .env
load_dotenv()

# Flask app initialization
app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",
    "https://me-profiled-frontend.vercel.app"
])

# PDF text extraction
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

# AI resume analyzer endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello from Backend"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400

    job_description = request.form.get('jobDescription', '')
    if not job_description:
        return jsonify({'error': 'No job description provided'}), 400

    resume_file = request.files['resume']
    resume_text = extract_text_from_pdf(io.BytesIO(resume_file.read()))

    if not resume_text:
        return jsonify({'error': 'Could not extract text from the resume PDF. The file might be empty, corrupted, or image-based.'}), 500

    try:
        # Define LLM
        llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0.2)

        # Prompt with scoring logic
        prompt_template = """
You are an expert AI career coach and resume analyzer.
Your goal is to provide a detailed, constructive analysis of a user's resume against a specific job description.

**Resume Content:**
{resume}

**Job Description:**
{job_description}

**Analysis Instructions:**

1. **Match Score Calculation:**  
   Calculate a final match score from 0 to 100 using the following weight distribution:
   - **Skills Match (50%)**: Check how many of the technical and soft skills from the job description are mentioned or implied in the resume.
   - **Experience Match (40%)**: Evaluate how well the candidate’s past roles, industries, and years of experience align with the job requirements.
   - **Keyword Match (10%)**: Identify important keywords from the job description (e.g., tools, technologies, frameworks, methodologies) and how many of them appear in the resume.

   Calculate individual scores for each of the three categories:
   matchScore = (skillsMatchPercent * 0.50) + (experienceMatchPercent * 0.40) + (keywordMatchPercent * 0.10)

   Round all percentage values and the final score to the nearest integer. A score of 85 or above indicates a strong match.

2. **Analysis Summary:**  
   Write a 2–3 sentence overview. Clearly state whether the candidate is a strong, moderate, or weak fit and summarize key alignment areas.

3. **Strengths:**  
   List 3–5 things the candidate does well that are directly relevant to the job (skills, technologies, experience, etc.).

4. **Areas for Improvement:**  
   List 3–5 areas where the resume could be improved to better match the job. Focus on **missing skills**, **important keywords**, or **experience gaps**. Be actionable and specific.

**Output Format:**  
Return the response strictly in the following JSON format. Do not include any other explanation or markdown formatting.

{{
    "matchScore": <number>,
    "skillsMatchPercent": <number>,
    "experienceMatchPercent": <number>,
    "keywordMatchPercent": <number>,
    "summary": "<string>",
    "strengths": ["<string>", "<string>", ...],
    "areasForImprovement": ["<string>", "<string>", ...]
}}
"""

        prompt = ChatPromptTemplate.from_template(prompt_template)
        parser = JsonOutputParser()
        chain = prompt | llm | parser

        # Invoke AI agent
        analysis_result = chain.invoke({
            "resume": resume_text,
            "job_description": job_description
        })

        return jsonify(analysis_result)

    except Exception as e:
        print(f"An error occurred during AI analysis: {e}")
        return jsonify({'error': 'Failed to get analysis from AI agent.'}), 500

# Start server
if __name__ == '__main__':
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in .env file. Please add it.")
    app.run(debug=True, port=5001)
