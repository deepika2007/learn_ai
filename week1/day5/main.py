import os
from pathlib import Path 
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

client = Groq(api_key=my_api_key)

# model="llama-3.3-70b-versatile"
model="openai/gpt-oss-120b"
role='user'


from pydantic import BaseModel

class Job_description(BaseModel):
    role:str
    required_skills:str
    min_experience:str
    educational_required:str
    responsibilities:str

job_schema = Job_description.model_json_schema()
response_format={"type": "json_object",}

jd= """
    We are seeking a highly skilled and motivated Software Engineer to join our dynamic team. The ideal candidate will have a strong background in software development, with expertise in Python, JavaScript, and cloud technologies.
    Responsibilities:
    - Develop and maintain web applications using Python and JavaScript.    
    - Collaborate with cross-functional teams to design, implement, and optimize software solutions.
    - Participate in code reviews and contribute to best practices for software development.
    - Stay up-to-date with emerging technologies and industry trends to ensure our software remains cutting-edge. 

"""

system_prompt = """You are a expert HR assistant. You have received the following job description through the user inputs: you have to extract the information as per the {job_schema} and provide the output in the following format(json)."""
message_system={"role": 'system', "content": system_prompt}

user_prompt = f"Job Description: {jd}\n\nPlease extract the information as per the job schema and provide the output in JSON format."
message_user={"role": 'user', "content": user_prompt}

messages=[message_system, message_user]
response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

answer=response.choices[0].message.content
print(f"Extracted Information: {answer}")



# Read Json Data from the response

import json
data_file= json.loads(answer)
ticket= Job_description(**data_file)

print(f"Role: {ticket.role}")
print(f"Required Skills: {ticket.required_skills}")
print(f"Minimum Experience: {ticket.min_experience}")
print(f"Educational Requirement: {ticket.educational_required}")
print(f"Responsibilities: {ticket.responsibilities}")



#  for the Resume screening

class Experience(BaseModel):
    company_name:str | None = None
    role:str | None = None
    duration:str | None = None
    skills_used:str
    description:str | None = None


class Resume(BaseModel):
    name:str | None = None
    email:str | None = None
    phone:str | None = None

    total_experience_years:str | None = None

    experiences:list[Experience]
    projects:list[str]
    skills:list[str]
    certifications:list[str]


class MatchResults(BaseModel):
    score:float
    details:dict


job_schema = Resume.model_json_schema()
response_format={"type": "json_object"}



def evaluate_resume(job: Job_description, resume: Resume) -> MatchResults:
    # Placeholder logic for evaluating the resume against the job description
    score = 0.0
    details = {}

    prompt = f"""
                You are an expert HR assistant. You have received the following job description and resume.
                {{"job": {job.json()}, "resume": {resume.json()}}}
                You need to evaluate the resume against the job description and provide a match score (0-100) 
                along with detailed feedback on how well the resume aligns with the job requirements.
                Provide the output in the following format:
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
        response_format={"type": "json_object",}
    )

    response_data = json.loads(response.choices[0].message.content)
    score = response_data.get("score", 0.0)
    details = response_data.get("details", {})

    return MatchResults(score=score, details=details)
    

