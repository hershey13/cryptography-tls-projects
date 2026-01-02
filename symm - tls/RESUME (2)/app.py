from flask import Flask, request, render_template
import requests
from PyPDF2 import PdfReader
import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="AIzaSyAQLetM2454Tj6WoKmm1t41EH5oXbNw-eE")  

model = genai.GenerativeModel(model_name="gemini-1.5-pro")

app = Flask(__name__)

# Load JD templates
def load_template(name):
    templates = {
        "software_engineer": "We are looking for a Software Engineer skilled in Python and React...",
        "data_scientist": "We are hiring a Data Scientist with expertise in machine learning and data analytics...",
        "product_manager": "Looking for a Product Manager with experience in agile and stakeholder management..."
    }
    return templates.get(name, "")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    jd_text = request.form.get('jd_text', "")
    jd_url = request.form.get('jd_url', "")
    jd_template = request.form.get('jd_template', "")
    resume_file = request.files.get('resume-upload')
    resume_text = ""

    if resume_file and resume_file.filename.endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_file)
    elif resume_file:
        resume_text = resume_file.read().decode('utf-8', errors='ignore')

    if jd_text.strip():
        jd = jd_text
    elif jd_url.strip():
        try:
            jd = requests.get(jd_url).text
        except:
            jd = ""
    elif jd_template:
        jd = load_template(jd_template)
    else:
        jd = ""

    prompt = f"""
    Compare the following resume with the job description.
    Return a score out of 100, and highlight strengths and areas to improve.

    Resume:
    {resume_text}

    Job Description:
    {jd}
    """

    try:
        gemini_response = model.generate_content(prompt)
        result_text = gemini_response.text
    except Exception as e:
        result_text = f"Error from Gemini: {e}"

    return render_template("result.html", result=result_text)


if __name__ == '__main__':
    app.run(debug=True)
