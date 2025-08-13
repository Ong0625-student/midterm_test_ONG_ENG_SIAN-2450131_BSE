# midterm_test_ONG_ENG_SIAN-2450131_BSE
# DEBUGGING_FINDINGS for demo.py

## Bug #1: Environment variables not loaded

**Error/Issue Observed:**
The program could not find the `GOOGLE_API_KEY` even though it was in the `.env` file.

**LLM Assistance Used:**
I use General Chat LLM check the code why `os.getenv("GOOGLE_API_KEY")` was not working and how to load `.env` files.

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
I use General Chat LLM check the tools and which ones were missing.

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

## Bug #3: Router did not use tools
**Error/Issue Observed:**
Even with tools added, the router did not process weather and calculator queries.

**LLM Assistance Used:**
I use General Chat LLM testing how to pass tools to ConversationRouter.

**Root Cause:**
The router was created with only llm, but it needed the tools too.

**Fix Applied:**

```python
Edit
router = ConversationRouter(llm, tools=tools)
```

## Bug #4: run_mock_demo() not defined
**Error/Issue Observed:**
If no GOOGLE_API_KEY was set, the program called run_mock_demo() and crashed.

**LLM Assistance Used:**
I use General Chat LLM testing how to fix this missing functions.

**Root Cause:**
The function run_mock_demo() was not in the script or imported.

Solve:

```python
from mock_demo import run_mock_demo  # Add this if the function exists
```

