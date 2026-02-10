Link to running app: https://claudea24-ai-hangman.streamlit.app/

Running locally: 

using pip:
1. setup the requirements by running `pip install -r requirements.txt`
2. add `OPENAI_API_KEY="your_api_key"` in `.env`
3. run the app: `streamlit run app.py`

using uv:
1. add the dependencies in `pyproject.toml` or `uv add streamlit openai python-dotenv`
2. add `OPENAI_API_KEY="your_api_key"` in `.env`
3. run the app: `uv run streamlit run app.py`
