import io
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from dotenv import load_dotenv

# Import LangChain components
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Load environment variables from .env file
load_dotenv()

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

def extract_text_from_pdf(pdf_file):
    """Extracts text from a given PDF file stream."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        # --- THIS IS THE FIX ---
        # We iterate through pdf_reader.pages, not pdf_reader itself.
        for page in pdf_reader.pages:
            # Ensure page.extract_text() doesn't return None
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        # Log the actual error for debugging
        print(f"Error reading PDF: {e}")
        return ""

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyzes the resume against the job description using an AI Agent."""
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    job_description = request.form.get('jobDescription', '')
    if not job_description:
        return jsonify({'error': 'No job description provided'}), 400

    resume_file = request.files['resume']
    resume_text = extract_text_from_pdf(io.BytesIO(resume_file.read()))
    
    if not resume_text:
        return jsonify({'error': 'Could not extract text from the resume PDF. The file might be empty, corrupted, or image-based.'}), 500

    # --- AI Agent Logic using LangChain ---
    try:
        # 1. Define the LLM for the agent
        llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0.2)

        # 2. Create the prompt template
        prompt_template = """
You are an expert AI career coach and resume analyzer.
Your goal is to provide a detailed, constructive analysis of a user's resume against a specific job description.

**Resume Content:**
{resume}

**Job Description:**
{job_description}

**Analysis Instructions:**
1. **Match Score:** Calculate a match score from 0 to 100, based on:
   - **Skills Match (40%)**: How many technical and soft skills from the job description appear in the resume.
   - **Experience Match (30%)**: Relevance of work experience, job roles, and duration compared to what's required.
   - **Keyword Match (30%)**: Match of important terms (technologies, responsibilities, industry-specific words).

   Provide a weighted score based on these three categories and include the percentage from each category in the final score calculation. A score of 85+ is considered a strong match.

2. **Analysis Summary:** Write a 2-3 sentence summary of your findings. Clearly state whether the candidate is a strong, moderate, or weak fit.

3. **Strengths:** List 3–5 key strengths that align well with the job description.

4. **Areas for Improvement:** List 3–5 important gaps. Include **missing keywords**, **skills**, or **experience** that would improve the match. Be actionable and specific.

**Output Format:**
Provide your response strictly in the following JSON format. Do not include any other text or markdown formatting.
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
        
        # 3. Define the output parser
        parser = JsonOutputParser()

        # 4. Create the agent chain
        chain = prompt | llm | parser

        # 5. Run the agent
        analysis_result = chain.invoke({
            "resume": resume_text,
            "job_description": job_description
        })

        return jsonify(analysis_result)

    except Exception as e:
        print(f"An error occurred during AI analysis: {e}")
        return jsonify({'error': 'Failed to get analysis from AI agent.'}), 500

if __name__ == '__main__':
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in .env file. Please add it.")
    app.run(debug=True, port=5001)

