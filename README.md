## LLM calls -> 
1. API KEY : Client -> Server (groq)
2. Model : exact name
3. Message : role (AI, Assistant, System) + content 
4. Response : choices + usages (tokens)


## for folders commands 
## day1
uv init day1
cd day1 and uv venv --python 3.11
source .venv/bin/activate (venv activate command)
uv add groq python-dotenv (groq- dependency in pyproject.toml)