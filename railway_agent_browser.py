# === Standard Library Imports ===
import asyncio
import os
import json
import re
from typing import List
from datetime import datetime, timedelta

# === Third-Party Library Imports ===
from pydantic import BaseModel
from browser_use import Controller, Agent
from browser_use.browser.context import BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from playwright.async_api import Page  # Add this import


# === Pydantic Output Model for Browser Controller ===
class TrainInfo(BaseModel):
    train_number: str
    train_name: str
    departure: str
    arrival: str
    duration: str
    fare: str
    available: str


class TrainAvailability(BaseModel):
    source: str
    destination: str
    date: str
    class_: str
    trains: List[TrainInfo]


# === Controller Setup ===
controller = Controller(output_model=TrainAvailability)


from playwright.async_api import Page

@controller.action("Clicks the travel class dropdown and selects the given class (like 1A, 2A, 3A, SL).")
async def select_travel_class(page: Page, class_name: str): 
    try:
        # Click the dropdown for travel class
        await page.click("//div[contains(@class, 'ui-dropdown-trigger') and contains(@class, 'ui-state-default')]")

        # Wait for the dropdown options to load
        await page.wait_for_selector("//ul[@role='listbox']", timeout=3000)

        # Locate the desired class using the provided XPath with contains()
        class_option = await page.query_selector(f"//li[contains(@aria-label, '{class_name}')]")
        if not class_option:
            raise ValueError(f"Class '{class_name}' not found in the dropdown.")
        
        # Scroll into view and add a delay to ensure proper scrolling
        await class_option.scroll_into_view_if_needed()
        await asyncio.sleep(2)  # Add a 2-second delay for stability

        # Click the desired class
        await class_option.click()

        print(f"✅ Successfully selected travel class: {class_name}")
    except Exception as e:
        print(f"❌ Failed to select class '{class_name}': {e}")


# === Extract Query Info ===
async def extract_query_details(user_query: str, llm) -> dict:
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)
    today_str = today.strftime("%Y-%m-%d")
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")

    prompt = f"""
You are a smart assistant that extracts train booking info from natural language.

Query: "{user_query}"

Return ONLY a valid JSON with the following keys:
- source
- destination
- class

Rules:
- Default class to "2A" if not mentioned.
- Do NOT include "date" in the response.
- Return ONLY valid JSON, no extra text or formatting.

Example:
{{
  "source": "Kolkata",
  "destination": "Mumbai",
  "class": "3AC"
}}
"""

    response = await llm.ainvoke(prompt)
    try:
        content = response.content if hasattr(response, "content") else str(response)
        cleaned = re.sub(r"```(?:json|python)?", "", content).strip("` \n")
        base_data = json.loads(cleaned)

        lower_query = user_query.lower()
        if "today" in lower_query:
            base_data["date"] = today_str
        else:
            base_data["date"] = tomorrow_str

        return base_data
    except Exception as e:
        print(f"❌ Failed to parse query details: {e}")
        print("Raw response:", response)
        return None


# === Main Agent Logic ===
async def railway_agent(user_query: str):
    print("\n🤖 Processing your query...")

    # Using env var for security
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("❌ GEMINI_API_KEY not set. Please export it in your environment.")

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)

    details = await extract_query_details(user_query, llm)
    if not details:
        print("⚠️ Could not extract travel details.")
        return

    source = details["source"]
    destination = details["destination"]
    travel_date = details["date"]
    travel_class = details["class"]

    print(f"🔍 Searching trains from {source} to {destination} on {travel_date} (Class: {travel_class})")

    task = f"""
    1. Open the IRCTC train search page: https://www.irctc.co.in/nget/train-search.
    2. In the 'From' field, type '{source}' and select the appropriate station from the dropdown.
    3. In the 'To' field, type '{destination}' and select the appropriate station from the dropdown.
    4. Set the journey date to '{travel_date}'.
    5. Use the controller action `select_travel_class` to select the travel class '{travel_class}'. (timeout: 5 seconds)
    6. Click the 'Search' button and wait for the train list to load (timeout: 5 seconds).
    7. Scroll to find the train results and click on the '{travel_class}' class fare option for each train.
    8. Extract details and return the train availability in JSON format using the TrainAvailability model.
    9. For every train returned, add "available": "yes" in the JSON.
    10. If "No direct trains available between the inputted stations" pop-up message appears, end task and show message "no trains available" and skip the rest of the steps.
    11. Ensure the output is a valid JSON object — do not escape or wrap in quotes. (timelimit: 15 seconds)
"""

    agent = Agent(task=task, controller=controller, llm=llm)
    history = await agent.run()

    result = history.final_result()
    print("\n📋 Final Result:\n", result)

    try:
        with open("train_results.json", "w") as f:
            json.dump(json.loads(result), f, indent=4)
        print("✅ Results saved to train_results.json")
    except Exception as e:
        print("❌ Failed to save result:", e)


# === CLI ===
async def main():
    print("🚆 Railway Assistant Ready!")
    print("Ask something like: 'Find trains from Korba to Delhi tomorrow in 1AC'")
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("🧾 Query: ")
        if user_query.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break
        await railway_agent(user_query)


if __name__ == "__main__":
    asyncio.run(main())