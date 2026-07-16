## LLM calls -> 
1. API KEY : Client -> Server (groq)
2. Model : exact name
3. Message : role (AI, Assistant, System) + content 
4. Response : choices + usages (tokens)

<!-- input token + output/completion = total token -->
## TOKENS - common re-usables words (text -> number -> LLM process -> number -> text) 

<!-- ## for folders commands  -->
## day1
<!-- -> include format for calling LLM -->
uv init day1
cd day1 & uv venv --python 3.11
source .venv/bin/activate (venv activate command)
uv add groq python-dotenv (groq- dependency in pyproject.toml)


## day2 
<!-- -> include temprature and system role for specific role -->
uv init day2
cd day2 & uv venv --python 3.11
source .venv/bin/activate (venv activate command)
uv add groq python-dotenv


## day3
<!-- -> understanding about tokenization and usages of token based on I/O token -->
uv init day3
cd day2 & uv venv --python 3.11
source .venv/bin/activate (venv activate command)
uv add groq python-dotenv
