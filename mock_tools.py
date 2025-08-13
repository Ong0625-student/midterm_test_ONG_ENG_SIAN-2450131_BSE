"""Mock tools for the LangChain application."""

import random
from typing import Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import datetime


# ---------------- Existing Tools ---------------- #

class WeatherSearchInput(BaseModel):
    """Input for weather search tool."""
    location: str = Field(description="The location to get weather for")


class FakeWeatherSearchTool(BaseTool):
    """A mock weather search tool that returns fake weather data."""
    
    name: str = "weather_search"
    description: str = "Get current weather information for a specific location"
    args_schema: type = WeatherSearchInput
    
    def _run(self, location: str) -> str:
        """Run the weather search tool."""
        conditions = ["sunny", "cloudy", "rainy", "snowy", "partly cloudy", "stormy"]
        temperatures = list(range(-10, 40))  # Celsius
        condition = random.choice(conditions)
        temperature = random.choice(temperatures)
        humidity = random.randint(30, 90)
        wind_speed = random.randint(0, 25)
        
        return f"""Weather in {location}:
- Condition: {condition}
- Temperature: {temperature}°C
- Humidity: {humidity}%
- Wind Speed: {wind_speed} km/h"""


class CalculatorInput(BaseModel):
    """Input for calculator tool."""
    expression: str = Field(description="Mathematical expression to evaluate")


class FakeCalculatorTool(BaseTool):
    """A mock calculator tool for basic math operations."""
    
    name: str = "calculator"
    description: str = "Perform basic mathematical calculations"
    args_schema: type = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """Run the calculator tool."""
        try:
            result = eval(expression)  # Fixed: removed +1 to show correct result
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Error calculating {expression}: {str(e)}"


class NewsSearchInput(BaseModel):
    """Input for news search tool."""
    topic: str = Field(description="The topic to search news for")


class FakeNewsSearchTool(BaseTool):
    """A mock news search tool that returns fake news headlines."""
    
    name: str = "news_search"
    description: str = "Search for recent news articles on a specific topic"
    args_schema: type = NewsSearchInput
    
    def _run(self, topic: str) -> str:
        """Run the news search tool."""
        headlines = [
            f"Breaking: Major developments in {topic} industry",
            f"Experts discuss the future of {topic}",
            f"New research reveals insights about {topic}",
            f"Local community responds to {topic} changes",
            f"Global impact of {topic} continues to grow"
        ]
        selected_headlines = random.sample(headlines, 5)
        return f"""Recent news about {topic}:
{chr(10).join(f"• {headline}" for headline in selected_headlines)}"""


# ---------------- Added a New Tool ---------------- #

# Add Code Start
class DateTimeInput(BaseModel):
    """Input for date and time tool."""
    location: str = Field(description="The location to get current date and time for")


class FakeDateTimeTool(BaseTool):
    """A mock date and time tool that returns the current date and time."""
    
    name: str = "date_time"
    description: str = "Get current date and time for a specific location"
    args_schema: type = DateTimeInput
    
    def _run(self, location: str) -> str:
        """Run the date and time tool."""
        now = datetime.datetime.now()
        return f"Current date and time in {location}: {now.strftime('%Y-%m-%d %H:%M:%S')}"

