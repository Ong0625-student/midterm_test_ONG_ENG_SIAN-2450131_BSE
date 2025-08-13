"""Demo script to showcase the LangChain application features."""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from mock_tools import FakeWeatherSearchTool, FakeCalculatorTool, FakeNewsSearchTool
from router import ConversationRouter

# Load environment variables from .env file
load_dotenv()  

# Optional: make sure run_mock_demo is imported if used
# from mock_demo import run_mock_demo   # Uncomment if this function exists


def run_demo():
    """Run a demonstration of the application features."""
    print("🚀 LangChain Application Demo")
    print("=" * 40)
    
    # Check if Google API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  No Google API key found. Using mock responses for demo.")
        run_mock_demo()  # Make sure this function exists/imported
        return
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Initialize all tools
    tools = [
        FakeNewsSearchTool(),
        FakeWeatherSearchTool(),
        FakeCalculatorTool()
    ]
    
    # Initialize router and pass the tools
    router = ConversationRouter(llm, tools=tools)
    
    # Demo queries
    demo_queries = [
        "What's the weather like in Tokyo?",
        "Calculate 5 * 3",
        "Find me news about machine learning",
        "Hello! How are you doing today?"
    ]
    
    print("\n🎯 Running demo queries...")
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n--- Demo {i} ---")
        print(f"Query: {query}")
        try:
            response = router.process_message(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    run_demo()



