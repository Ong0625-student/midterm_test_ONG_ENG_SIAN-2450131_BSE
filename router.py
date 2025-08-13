"""LangChain router implementation for handling different query types."""

from typing import List
from langchain.schema import BaseMessage
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import BaseTool


class QueryRouter:
    """Routes queries to appropriate tools based on content analysis."""

    def __init__(self, llm: ChatGoogleGenerativeAI, tools: List[BaseTool]):
        self.llm = llm
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in tools}

        # -------------------------------
        # Change 1: Customize the routing prompt
        # -------------------------------
        self.routing_prompt = PromptTemplate(
            input_variables=["query", "available_tools"],
            template=(
                "You are a smart assistant. "
                "Choose the best tool for this query from the list below:\n"
                "{available_tools}\n"
                "Query: {query}\n"
                "Answer only with the tool name or 'general_chat'."
            )
        )

        # Create routing chain
        self.routing_chain = self.routing_prompt | self.llm | StrOutputParser()

        # -------------------------------
        # Change 2: Add the new routing strategy
        # Simple keyword-based fallback if LLM fails
        # -------------------------------
        self.keyword_routing = {
            "weather": "FakeWeatherSearchTool",
            "calculate": "FakeCalculatorTool",
            "news": "FakeNewsSearchTool"
        }

    def route_query(self, query: str) -> str:
        """Route a query to the appropriate tool."""
        # Prepare tool descriptions
        tool_descriptions = [f"- {tool.name}: {tool.description}" for tool in self.tools]
        available_tools = "\n".join(tool_descriptions)

        # Try LLM routing first
        result = self.routing_chain.invoke({
            "query": query,
            "available_tools": available_tools
        })

        tool_name = result.strip()

        # -------------------------------
        # Change 3: Apply the keyword-based fallback
        # -------------------------------
        if tool_name not in self.tool_map:
            query_lower = query.lower()
            for keyword, tool in self.keyword_routing.items():
                if keyword in query_lower:
                    tool_name = tool
                    break
            else:
                tool_name = "general_chat"

        return tool_name

    def execute_tool(self, tool_name: str, query: str) -> str:
        """Execute the selected tool with the query."""
        if tool_name not in self.tool_map:
            return "I'm not sure how to help with that. Please rephrase."

        tool = self.tool_map[tool_name]

        # -------------------------------
        # Change 4: Customize the parameter to extraction prompt
        # -------------------------------
        param_extraction_prompt = PromptTemplate(
            input_variables=["query", "tool_description"],
            template=(
                "You are a helpful assistant. "
                "Extract the main input from the query to use with this tool:\n"
                "{tool_description}\n"
                "Query: {query}\n"
                "Return only the input needed by the tool."
            )
        )

        param_chain = param_extraction_prompt | self.llm | StrOutputParser()
        parameter = param_chain.invoke({
            "query": query,
            "tool_description": tool.description
        }).strip()

        try:
            return tool._run(parameter)
        except Exception as e:
            return f"Error executing tool: {str(e)}"


class ConversationRouter:
    """Advanced router that maintains conversation context."""

    def __init__(self, llm: ChatGoogleGenerativeAI, tools: List[BaseTool]):
        self.llm = llm
        self.query_router = QueryRouter(llm, tools)
        self.conversation_history = []

    def process_message(self, message: str) -> str:
        """Process a message with conversation context."""
        # Save user message
        self.conversation_history.append({"role": "user", "content": message})

        # Route the query
        tool_name = self.query_router.route_query(message)

        if tool_name == "general_chat":
            response = self._handle_general_chat(message)
        else:
            response = self.query_router.execute_tool(tool_name, message)

        # Save assistant response
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def _handle_general_chat(self, message: str) -> str:
        """Handle general conversation that doesn't require tools."""
        context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.conversation_history[-4:]  # Last 4 messages
        ])

        # -------------------------------
        # Change 5: Customize the general chat prompt
        # -------------------------------
        general_prompt = PromptTemplate(
            input_variables=["context", "message"],
            template=(
                "You are a friendly assistant. "
                "Use the conversation context to reply naturally.\n"
                "Context: {context}\n"
                "Message: {message}"
            )
        )

        general_chain = general_prompt | self.llm | StrOutputParser()
        return general_chain.invoke({"context": context, "message": message})

