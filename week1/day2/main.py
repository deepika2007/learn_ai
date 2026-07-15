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
prompt="suggest a name for my learning course on AI and ML"

message_system={"role":"system", "content":"You are brand and application manager for my course."}
message={"role": role, "content": prompt}


messages=[message_system, message]

# an paramerters can be added to the create method to customize the response. For example, you can set the temperature (for creativity) and max_tokens parameters to control the randomness and length of the response.
response = client.chat.completions.create(model=model, messages=messages, temperature=2, max_tokens=100)
print(response.choices[0].message.content)