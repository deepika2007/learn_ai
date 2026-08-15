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
python main.py


## day2 
<!-- -> include temprature and system role for specific role -->
uv init day2
cd day2 & uv venv --python 3.11
source .venv/bin/activate (venv activate command)
uv add groq python-dotenv
python main.py


## day3
<!-- -> understanding about tokenization and usages of token based on I/O token -->
uv init day3
cd day3 & uv venv --python 3.11
source .venv/bin/activate (venv activate command)
uv add groq python-dotenv
python main.py


## day4
<!-- -> understanding about pydantic so that manage response with json pattern  -->
uv init day4
cd day4 & uv venv --python 3.11
source .venv/bin/activate (venv activate command)
uv add groq python-dotenv pydantic
python main.py


## day5
<!-- -> understanding for pypdf and python docs code for resume reader  -->
uv init day5
cd day5 & uv venv --python 3.11
source .venv/bin/activate (venv activate command)
uv add groq python-dotenv pydantic pypdf python-docx
python main.py