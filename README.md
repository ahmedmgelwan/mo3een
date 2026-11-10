# Mo3een
AI assistant to chat with your data

## Install

``` bash
cp .env.example .env
pip install uv
uv sync
```
## Run

```bash
uvicorn src.api.main:app --reload --port 8000
PYTHONPATH=. uv run streamlit run src/app/main.py
```