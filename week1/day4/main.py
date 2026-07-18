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


text='Hello my name is Deepika. I purchase iPhone from your store. I am facing issue with the product. I want to return the product and get my money back. Please help me with the process. My contact is 1234567890. My mail is deepika@example.com. Thank you.'


from pydantic import BaseModel

class Ticket(BaseModel):
    customer_name:str
    product_name:str
    issue_description:str
    contact_number:str
    email_id:str

schema = Ticket.model_json_schema()
response_format={"type": "json_object",}


system_prompt = f"""You are a customer support agent. You have received the following message from a customer: {text}, you have to extract the information as per the {schema} and provide the output in the following format(json)."""

message_system={"role": role, "content": system_prompt}

messages=[message_system]
response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

answer=response.choices[0].message.content
print(f"Extracted Information: {answer}")



# Read Json Data from the response

import json
data_file= json.loads(answer)
ticket= Ticket(**data_file)

print(f"Customer Name: {ticket.customer_name}")
print(f"Product Name: {ticket.product_name}")
print(f"Issue Description: {ticket.issue_description}")
print(f"Contact Number: {ticket.contact_number}")
print(f"Email ID: {ticket.email_id}")
