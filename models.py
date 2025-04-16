import os
import asyncio
import json
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, Controller

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Create controller for browser-use
controller = Controller()

# Initialize the LLM (OpenAI) - you can use ChatOpenAI or your LLaMA model based on your setup
llm = ChatOpenAI(model="gpt-4")

# Initialize the browser instance
browser = Browser()

# Define the railway agent
async def railway_agent(user_query: str) -> Dict[str, Any]:
    """
    Railway agent that uses browser-use to check train availability
    Args:
    user_query: Natural language query about train availability
    Returns:
    Dictionary with structured train information
    """
    # Ensure max_steps is an integer (set a max step value to avoid endless loops)
    max_steps = 10  # You can adjust this as needed

    # Create the agent for browsing and query processing
    agent = Agent(
        task="Find train availability between Indian cities",
        llm=llm,
        browser=browser
    )

    # Run the agent and get the response
    print(f"Searching with query: {user_query}")
    response = await agent.run(user_query, max_steps=max_steps)

    # Process and return the results
    return {
        "source": "Delhi",  # Replace with parsed source city from user query
        "destination": "Uttarakhand",  # Replace with parsed destination city
        "date": datetime.now().strftime("%Y-%m-%d"),
        "class": "3AC",  # Replace this with logic to parse class from user query
        "trains": response  # Assuming the agent's response contains the required train data
    }

# Main method to interact with the user
async def main():
    print("🚆 Welcome to the Railway Booking Assistant with Browser Automation 🚆")
    print("I can help you find train availability between cities in India.")
    print("Ask me questions like: 'Find trains from Delhi to Mumbai tomorrow for 3AC class'")
    print("Type 'exit' to quit.")

    while True:
        user_query = input("\nWhat would you like to know about train availability? (or 'exit' to quit): ")
        if user_query.lower() in ["exit", "quit", "bye"]:
            print("Thank you for using the Railway Booking Assistant. Happy travels! 👋")
            break
        print("\nSearching for train information...")
        print("This may take a moment as the browser navigates to Goibibo...")
        response = await railway_agent(user_query)
        print("\nResults:")
        print(json.dumps(response, indent=2))

if __name__ == "__main__":
    asyncio.run(main())