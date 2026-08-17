import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from reader import read_document
from pydantic import BaseModel

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

client = Groq(api_key=my_api_key)

# model="llama-3.3-70b-versatile"
model = "openai/gpt-oss-120b"
role = 'user'


class Job_description(BaseModel):
    role: str
    required_skills: str
    min_experience: str
    educational_required: str
    responsibilities: str


job_schema = Job_description.model_json_schema()
response_format = {"type": "json_object"}

jd = """
    We are seeking a highly skilled and motivated Software Engineer to join our dynamic team. The ideal candidate will have a strong background in software development, with expertise in Python, JavaScript, and cloud technologies.
    Responsibilities:
    - Develop and maintain web applications using Python and JavaScript.    
    - Collaborate with cross-functional teams to design, implement, and optimize software solutions.
    - Participate in code reviews and contribute to best practices for software development.
    - Stay up-to-date with emerging technologies and industry trends to ensure our software remains cutting-edge. 

"""

system_prompt = (
    "You are an expert HR assistant. Extract the information from the job description "
    "according to the following JSON schema:\n"
    f"{json.dumps(job_schema)}\n"
    "Ensure all fields are extracted as strings exactly as defined in the schema."
)
message_system = {"role": 'system', "content": system_prompt}

user_prompt = f"Job Description: {jd}\n\nPlease extract the information as per the job schema and provide the output in JSON format."
message_user = {"role": 'user', "content": user_prompt}

messages = [message_system, message_user]
response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

answer = response.choices[0].message.content
print(f"Extracted Information: {answer}")


# Read Json Data from the response
data_file = json.loads(answer)
job_description_text = Job_description(**data_file)
print('job_description_text', job_description_text)


# for the Resume screening
class Experience(BaseModel):
    company_name: str | None = None
    role: str | None = None
    duration: str | None = None
    skills_used: str
    description: str | None = None


class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_years: str | None = None

    experiences: list[Experience]
    projects: list[str]
    skills: list[str]
    certifications: list[str]


class MatchResults(BaseModel):
    score: float
    details: dict


def evaluate_resume(job: Job_description, resume: Resume) -> MatchResults:
    # Placeholder logic for evaluating the resume against the job description
    score = 0.0
    details = {}

    prompt = f"""
                You are an expert HR assistant. You have received the following job description and resume.
                {{"job": {job.model_dump_json()}, "resume": {resume.model_dump_json()}}}
                You need to evaluate the resume against the job description and provide a match score (0-100) 
                along with detailed feedback on how well the resume aligns with the job requirements.
                Provide the output in the following JSON format:
                {{
                    "score": float,
                    "details": {{
                        "name": str,
                        "email": str,
                        "phone": str,
                        "skills_match": str,
                        "experience_match": str,
                        "education_match": str,
                        "responsibilities_match": str,
                        "overall_feedback": str
                    }}
                }}
            """

    response = client.chat.completions.create(
        model=model,    
        messages=[{"role": "system", "content": prompt}],
        response_format={"type": "json_object"}
    )

    response_data = json.loads(response.choices[0].message.content)
    score = response_data.get("score", 0.0)
    details = response_data.get("details", {})

    return MatchResults(score=score, details=details)


def extract_resume_data(resume_text: str) -> Resume:
    resume_schema = Resume.model_json_schema()
    system_prompt = (
        "You are an expert HR assistant. Parse the following resume text and extract "
        "the information according to the following JSON schema:\n"
        f"{json.dumps(resume_schema)}\n"
        "Ensure all fields match the schema type and structure exactly. Return a valid JSON object."
    )
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Resume Text:\n{resume_text}"}
        ],
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content
    data = json.loads(content)
    
    # Ensure experiences is a list, and each has skills_used as string
    if "experiences" in data and isinstance(data["experiences"], list):
        for exp in data["experiences"]:
            if "skills_used" not in exp or exp["skills_used"] is None:
                exp["skills_used"] = ""
            elif isinstance(exp["skills_used"], list):
                exp["skills_used"] = ", ".join(exp["skills_used"])
    
    # Ensure projects, skills, certifications are lists of strings
    for field in ["projects", "skills", "certifications"]:
        if field not in data or not isinstance(data[field], list):
            data[field] = []
        else:
            data[field] = [str(x) for x in data[field]]
            
    if "experiences" not in data or not isinstance(data["experiences"], list):
        data["experiences"] = []
        
    return Resume(**data)


resume_folder = Path("resumes")
all_results = []

for resume_file in resume_folder.iterdir():
    if not resume_file.is_file() or resume_file.name.startswith('.'):
        continue
    resume_text = read_document(resume_file)
    time.sleep(5)  # Add a delay of 5 seconds between requests
    
    parsed_resume = extract_resume_data(resume_text)
    evaluation_result = evaluate_resume(job_description_text, parsed_resume)
    
    time.sleep(5)  # Add a delay of 5 seconds between requests
    all_results.append({
        "resume_file": resume_file.name,
        "score": evaluation_result.score,
        "details": evaluation_result.details
    })  


all_results.sort(key=lambda x: x["score"], reverse=True)

top_5_results = all_results[:5]
worst_results = all_results[-5:]

print("\n--- Evaluation Results ---")
for idx, res in enumerate(all_results, 1):
    print(f"{idx}. {res['resume_file']} - Score: {res['score']}")
    print(f"   Details: {json.dumps(res['details'], indent=2)}")
