import asyncio
import os
import json
import re
from typing import List
from pydantic import BaseModel, SecretStr
from datetime import datetime, timedelta

from browser_use import Controller, Agent
from langchain_google_genai import ChatGoogleGenerativeAI


# === Pydantic Output Model for Browser Controller ===
class TrainInfo(BaseModel):
    train_number: str
    train_name: str
    departure: str
    arrival: str
    duration: str
    fare: str


class TrainAvailability(BaseModel):
    source: str
    destination: str
    date: str
    trains: List[TrainInfo]


# === Controller Setup ===
controller = Controller(output_model=TrainAvailability)


# === Extract Query Info Using Gemini ===
async def extract_query_details(user_query: str, llm) -> dict:
    prompt = f"""
You are a smart assistant that extracts travel info from queries.

Query: "{user_query}"

Return ONLY a valid JSON object with the following keys:
- source
- destination
- date (in YYYY-MM-DD format)
- travel_class

Rules:
- If the date is "today", use today's date.
- If it's "tomorrow", use tomorrow's date.
- If class is not mentioned, default to "2AC".
- Return ONLY valid JSON. Do NOT wrap it in markdown or give explanation.

Example output:
{{
  "source": "Bangalore",
  "destination": "Delhi",
  "date": "2025-04-21",
  "travel_class": "2AC"
}}
"""

    response = await llm.ainvoke(prompt)

    try:
        response_text = response.content if hasattr(response, "content") else str(response)

        # Clean up accidental ```json or ```python markdown blocks
        cleaned = re.sub(r"```(?:json|python)?", "", response_text).strip("` \n")

        return json.loads(cleaned)

    except Exception as e:
        print(f"❌ Failed to parse query details: {e}")
        print("🔎 Raw response:", response_text)
        return None


# === Main Agent Function ===
async def railway_agent(user_query: str):
    print("\n🤖 Processing your query...")

    api_key = os.environ.get("GOOGLE_API_KEY", "your-google-api-key")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=SecretStr(api_key))

    details = await extract_query_details(user_query, llm)
    if not details:
        print("⚠️ Could not extract travel details from query.")
        return

    source = details["source"]
    destination = details["destination"]
    travel_date = details["date"]
    travel_class = details["travel_class"]

    print(f"🔍 Searching trains from {source} to {destination} on {travel_date} (Class: {travel_class})")

    task = f"""
    1. Open the IRCTC train search page: https://www.irctc.co.in/nget/train-search.
    2. In the 'From' field, type '{source}' and select the appropriate station.
    3. In the 'To' field, type '{destination}' and select the appropriate station.
    4. Set the journey date to '{travel_date}'.
    5. Click on the “Class” dropdown and scroll if necessary. Select the class matching '{travel_class}'. (timelimit: 5 seconds)
    6. Click the 'Search' button and wait for the train list to load (timeout: 5 seconds).
    7. Click on 2A option for train dsiplayed.
    8. Extract train availability and return it as JSON using the TrainAvailability model, also give fare proper rs format.
    Ensure the output is a valid JSON object — no escaping or wrapping. (timelimit: 15 seconds)
    """

    agent = Agent(task=task, controller=controller, llm=llm)
    history = await agent.run()
    history.save_to_file("test_validation.json")

    result = history.final_result()
    print("\n📋 Train Availability Result:\n")
    print(result)

    try:
        result_json = json.loads(result) if isinstance(result, str) else result
        with open("train_results.json", "w",  encoding="utf-8") as f:
            json.dump(result_json, f, indent=4, ensure_ascii=False)
        print("\n✅ Results saved to train_results.json")
    except Exception as e:
        print("❌ Error saving result:", e)


# === CLI Loop ===
async def main():
    print("🚆 Welcome to the Railway Booking Assistant!")
    print("Ask me to find train availability using natural language.")
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("🗣️ Your query: ")
        if user_query.lower() in ["exit", "quit"]:
            print("👋 Goodbye! Safe travels.")
            break

        await railway_agent(user_query)


# === Entry Point ===
if __name__ == "__main__":
    asyncio.run(main())
    
# import asyncio
# import os
# import json
# import re
# from typing import List
# from pydantic import BaseModel, SecretStr
# from datetime import datetime, timedelta

# from browser_use import Controller, Agent
# from langchain_google_genai import ChatGoogleGenerativeAI


# # === Pydantic Output Model for Browser Controller ===
# class TrainInfo(BaseModel):
#     train_number: str
#     train_name: str
#     departure: str
#     arrival: str
#     duration: str
#     fare: str


# class TrainAvailability(BaseModel):
#     source: str
#     destination: str
#     date: str
#     trains: List[TrainInfo]


# # === Controller Setup ===
# controller = Controller(output_model=TrainAvailability)


# # === Extract Query Info Using Gemini ===
# async def extract_query_details(user_query: str, llm) -> dict:
#     # Get today's and tomorrow's date as fallback
#     today = datetime.today().date()
#     tomorrow = today + timedelta(days=1)
#     today_str = today.strftime("%Y-%m-%d")
#     tomorrow_str = tomorrow.strftime("%Y-%m-%d")

#     prompt = f"""
# You are a smart assistant that extracts travel info from queries.

# Query: "{user_query}"

# Return ONLY a valid JSON object with the following keys:
# - source
# - destination
# - travel_class

# Rules:
# - If class is not mentioned, default to "2AC".
# - Do NOT include "date" in the response.
# - Return ONLY valid JSON. Do NOT wrap it in markdown or give explanation.

# Example output:
# {{
#   "source": "Bangalore",
#   "destination": "Delhi",
#   "travel_class": "2AC"
# }}
# """

#     response = await llm.ainvoke(prompt)

#     try:
#         response_text = response.content if hasattr(response, "content") else str(response)

#         # Remove possible markdown formatting
#         cleaned = re.sub(r"```(?:json|python)?", "", response_text).strip("` \n")
#         base_data = json.loads(cleaned)

#         # Infer date from user query
#         lower_query = user_query.lower()
#         if "today" in lower_query:
#             travel_date = today_str
#         elif "tomorrow" in lower_query:
#             travel_date = tomorrow_str
#         else:
#             # Default to tomorrow if no mention
#             travel_date = tomorrow_str

#         base_data["date"] = travel_date
#         return base_data

#     except Exception as e:
#         print(f"❌ Failed to parse query details: {e}")
#         print("🔎 Raw response:", response_text)
#         return None


# # === Main Agent Function ===
# async def railway_agent(user_query: str):
#     print("\n🤖 Processing your query...")

#     api_key = os.environ.get("GOOGLE_API_KEY", "your-google-api-key")
#     llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=SecretStr(api_key))

#     details = await extract_query_details(user_query, llm)
#     if not details:
#         print("⚠️ Could not extract travel details from query.")
#         return

#     source = details["source"]
#     destination = details["destination"]
#     travel_date = details["date"]
#     travel_class = details["travel_class"]

#     print(f"🔍 Searching trains from {source} to {destination} on {travel_date} (Class: {travel_class})")

#     # Build task for the browser agent
#     task = f"""
#     1. Open the IRCTC train search page: https://www.irctc.co.in/nget/train-search.
#     2. In the 'From' field, type '{source}' and select the appropriate station from the dropdown.
#     3. In the 'To' field, type '{destination}' and select the appropriate station from the dropdown.
#     4. Set the journey date to '{travel_date}'.
#     5. Choose '{travel_class}' class from the dropdown menu.
#     6. Click the 'Search' button and wait for the train list to load (timeout: 5 seconds).
#     7. Click on the 2A option for the train displayed.
#     8. Extract details and return the train availability in JSON format using the TrainAvailability model. 
#     Ensure the output is a valid JSON object — do not escape or wrap in quotes. (timelimit: 15 seconds)
#     """

#     agent = Agent(task=task, controller=controller, llm=llm)
#     history = await agent.run()
#     history.save_to_file("test_validation.json")

#     result = history.final_result()
#     print("\n📋 Train Availability Result:\n")
#     print(result)

#     try:
#         result_json = json.loads(result) if isinstance(result, str) else result
#         with open("train_results.json", "w", encoding="utf-8") as f:
#             json.dump(result_json, f, indent=4, ensure_ascii=False)
#         print("\n✅ Results saved to train_results.json")
#     except Exception as e:
#         print("❌ Error saving result:", e)


# # === CLI Loop ===
# async def main():
#     print("🚆 Welcome to the Railway Booking Assistant!")
#     print("Ask me to find train availability using natural language.")
#     print("Type 'exit' to quit.\n")

#     while True:
#         user_query = input("🗣️ Your query: ")
#         if user_query.lower() in ["exit", "quit"]:
#             print("👋 Goodbye! Safe travels.")
#             break

#         await railway_agent(user_query)


# # === Entry Point ===
# if __name__ == "__main__":
#     asyncio.run(main())    