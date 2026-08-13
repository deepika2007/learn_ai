import os
from pathlib import Path 
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

client = Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"
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


system_prompt = """You are a expert HR assistant. You have received the following job description through the user inputs: you have to extract the information as per the {job_schema} and provide the output in the following format(json)."""

message_system={"role": 'system', "content": system_prompt}

messages=[message_system]
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
    company_name:str
    role:str
    duration:str
    skills_used:str
    description:str


class Resume(BaseModel):
    name:str
    email:str
    phone:str
    total_experience_years:str
    experiences:list[Experience]
    projects:list[str]
    skills:list[str]
    certifications:list[str]


job_schema = Resume.model_json_schema()
response_format={"type": "json_object",}