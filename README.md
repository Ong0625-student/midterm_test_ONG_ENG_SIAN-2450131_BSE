# midterm_test_ONG_ENG_SIAN-2450131_BSE
# DEBUGGING_FINDINGS

## Bug #1: Environment variables not loaded

**Error/Issue Observed:**
The program could not find the `GOOGLE_API_KEY` even though it was in the `.env` file.

**LLM Assistance Used:**
I check the code why `os.getenv("GOOGLE_API_KEY")` was not working and how to load `.env` files.

**Root Cause:**
The code had a commented line `# os.environ[]` and did not use `load_dotenv()`, so environment variables were not loaded.

**Fix Applied:**
```python
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

````

## Bug #2: Missing tools for demo queries
Error/Issue Observed:
The program could not answer queries like "What's the weather like in Tokyo?" or "Calculate 5 * 3".

**LLM Assistance Used:**
I asked ChatGPT to check the tools and which ones were missing.

**Root Cause:**
Only FakeNewsSearchTool() was included. Weather and calculator tools were missing.

**Fix Applied:**

```python

tools = [
    FakeNewsSearchTool(),
    FakeWeatherSearchTool(),
    FakeCalculatorTool()
]
```
