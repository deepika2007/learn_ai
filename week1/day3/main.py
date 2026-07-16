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

prompt1="Hi"
prompt2= "What is the capital of France?"
prompt3="eassy for my cow into 500 words "

prompts=[prompt1, prompt2, prompt3]
for p in prompts:
    message={"role": role, "content": p}
    messages=[message]
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=100)
    usage = response.usage
    # print(response.choices[0], response)
    print(f"""Prompt {p} --->token usage: {usage.prompt_tokens} 
        prompt tokens, {usage.completion_tokens} completion tokens, {usage.total_tokens} total tokens""")

