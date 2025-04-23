# import os
# import asyncio
# import json
# from typing import Dict, Any, List
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from browser_use import Agent, Browser, Controller
# from pydantic import SecretStr

# # Load environment variables
# load_dotenv()

# # Set Google API key (replace with your actual key or load from .env)
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "AIzaSyAHNTgXjpYON9rDBClw-SlugX1c1IGBdjo")

# # Create controller (not used yet, but ready)
# controller = Controller()

# async def railway_agent() -> Dict[str, Any]:
#     """
#     Railway agent that uses browser-use to check train availability for a fixed task.
#     """
#     # Initialize LLM with Gemini
#     api_key = os.environ["GOOGLE_API_KEY"]
#     try:
#         llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(api_key))
#     except Exception as e:
#         print(f"Error initializing Gemini LLM: {str(e)}")
#         return {"source": "Korba", "destination": "Delhi", "date": "2025-04-18", "class": "2A", "trains": [], "error": f"LLM initialization failed: {str(e)}"}

#     # Initialize Browser
#     try:
#         browser = Browser()
#     except Exception as e:
#         print(f"Error initializing Browser: {str(e)}")
#         return {"source": "Korba", "destination": "Delhi", "date": "2025-04-18", "class": "2A", "trains": [], "error": f"Browser initialization failed: {str(e)}"}

#     # Define task with all instructions
#     task = """
#     You are a railway booking assistant tasked with finding train availability on the IRCTC website using a Playwright-based browser.
#     Follow these steps precisely:
#     1. Navigate to https://www.irctc.co.in/nget/train-search.
#     2. In the 'From' field, type 'KORBA - KRBA' and select 'KORBA - KRBA (CHAMPA)' from the dropdown.
#     3. In the 'To' field, type 'DELHI - DLI' and select 'DELHI - DLI (NEW DELHI)' from the dropdown.
#     4. Click the date field to open the calendar (showing April 2025). Verify 'April 2025' is displayed, then select '18' to set 18-04-2025. Ensure the date field shows '18-04-2025'.
#     5. Select '2A (Second AC)' from the class dropdown.
#     6. Click the 'Search' button (XPath: //*[@id="divMain"]//button[contains(text(), 'Search')] or //button[@type="submit"]).
#     7. Wait up to 20 seconds for the train list to load. Extract details for all available trains from the results table, including:
#        - train_number: Unique number (e.g., '18237').
#        - train_name: Name (e.g., 'Korba Express').
#        - departure: Departure time (e.g., '11:33').
#        - arrival: Arrival time (e.g., '14:50').
#        - duration: Travel duration (e.g., '27h 17m').
#        - availability: 2A class availability (e.g., 'Available 10' or 'WL 5').
#        - fare: 2A class fare (e.g., '2450').
#     8. If no trains are found or the list is empty, return an empty list.
#     9. If a CAPTCHA appears, notify the user for manual solving or return an error in the JSON. If login is required, include an error message in the JSON.
#     10. If station codes or date are invalid, try 'NEW DELHI - NDLS' for Delhi and note the attempt in the JSON.
#     Return a structured JSON object with fields: source (Korba), destination (Delhi), date (2025-04-18), class (2A), trains (list of train details), and error (null or error message if applicable).
#     """

#     # Create and run the Agent
#     try:
#         agent = Agent(task=task, llm=llm, browser=browser)
#     except Exception as e:
#         print(f"Error initializing Agent: {str(e)}")
#         return {"source": "Korba", "destination": "Delhi", "date": "2025-04-18", "class": "2A", "trains": [], "error": f"Agent initialization failed: {str(e)}"}

#     # Run the agent and get results
#     try:
#         result = await agent.run()
#         print("Result:", result)  # Debug: Inspect result format
#     except Exception as e:
#         print(f"Error during agent execution: {str(e)}")
#         result = {"trains": [], "error": f"Agent execution failed: {str(e)}"}

#     # Construct JSON output
#     json_output = {
#         "source": "Korba",
#         "destination": "Delhi",
#         "date": "2025-04-18",
#         "class": "2A",
#         "trains": [],
#         "error": result.get("error", None)
#     }

#     # Process result (assume result is a dict with train details)
#     trains = result.get("trains", [])
#     if trains and isinstance(trains, list):
#         json_output["trains"] = [
#             {
#                 "train_number": train.get("train_number", "unknown"),
#                 "train_name": train.get("train_name", "unknown"),
#                 "departure": train.get("departure", "unknown"),
#                 "arrival": train.get("arrival", "unknown"),
#                 "duration": train.get("duration", "unknown"),
#                 "availability": train.get("availability", "unknown"),
#                 "fare": str(train.get("fare", "unknown"))
#             }
#             for train in trains
#         ]

#     # Save JSON output to a file
#     output_file = "train_results.json"
#     with open(output_file, "w") as f:
#         json.dump(json_output, f, indent=2)

#     # Print JSON output
#     print("\nResults:")
#     print(json.dumps(json_output, indent=2))

#     # List directory contents to locate trace/agent files
#     print("Directory contents:", os.listdir("."))

#     return json_output

# async def main():
#     """
#     Execute the railway agent to fetch train availability from Korba to Delhi.
#     """
#     print("🚆 Running Railway Booking Assistant with Browser Automation 🚆")
#     print("Fetching trains from Korba to Delhi on April 18, 2025, for 2A class...")
#     print("This may take a moment as the browser navigates to IRCTC...")
    
#     response = await railway_agent()
    
#     print("🚆 Search completed! 🚆")

# if __name__ == "__main__":
#     asyncio.run(main())


# import os
# import asyncio
# import json
# from typing import Dict, Any, List
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from browser_use import Agent, Browser, Controller
# from pydantic import SecretStr

# # Load environment variables
# load_dotenv()

# # Set Google API key (replace with your actual key or load from .env)
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "AIzaSyAHNTgXjpYON9rDBClw-SlugX1c1IGBdjo")

# # Create controller (not used yet, but ready)
# controller = Controller()

# async def railway_agent() -> Dict[str, Any]:
#     """
#     Railway agent that uses browser-use to check train availability for a fixed task.
#     """
#     # Initialize LLM with Gemini
#     api_key = os.environ["GOOGLE_API_KEY"]
#     try:
#         llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(api_key))
#     except Exception as e:
#         print(f"Error initializing Gemini LLM: {str(e)}")
#         return {"source": "Korba", "destination": "Delhi", "date": "2025-04-18", "class": "2A", "trains": [], "error": f"LLM initialization failed: {str(e)}"}

#     # Initialize Browser
#     try:
#         browser = Browser()
#     except Exception as e:
#         print(f"Error initializing Browser: {str(e)}")
#         return {"source": "Korba", "destination": "Delhi", "date": "2025-04-18", "class": "2A", "trains": [], "error": f"Browser initialization failed: {str(e)}"}

#     # Define task with all instructions
#     task = """
#     You are a railway booking assistant tasked with finding train availability on the IRCTC website using a Playwright-based browser.
#     Follow these steps precisely:
#     1. Navigate to https://www.irctc.co.in/nget/train-search.
#     2. In the 'From' field, type 'KORBA - KRBA' and select 'KORBA - KRBA (CHAMPA)' from the dropdown.
#     3. In the 'To' field, type 'DELHI - DLI' and select 'DELHI - DLI (NEW DELHI)' from the dropdown.
#     4. Click the date field to open the calendar (showing April 2025). Verify 'April 2025' is displayed, then select '18' to set 18-04-2025. Ensure the date field shows '18-04-2025'.
#     5. Select '2A (Second AC)' from the class dropdown.
#     6. Click the 'Search' button (XPath: //*[@id="divMain"]//button[contains(text(), 'Search')] or //button[@type="submit"]).
#     7. Wait up to 20 seconds for the train list to load. Extract details for all available trains from the results table, including:
#        - train_number: Unique number (e.g., '18237').
#        - train_name: Name (e.g., 'Korba Express').
#        - departure: Departure time (e.g., '11:33').
#        - arrival: Arrival time (e.g., '14:50').
#        - duration: Travel duration (e.g., '27h 17m').
#        - availability: 2A class availability (e.g., 'Available 10' or 'WL 5').
#        - fare: 2A class fare (e.g., '2450').
#     8. If no trains are found or the list is empty, return an empty list.
#     9. If a CAPTCHA appears, notify the user for manual solving or return an error in the JSON. If login is required, include an error message in the JSON.
#     10. If station codes or date are invalid, try 'NEW DELHI - NDLS' for Delhi and note the attempt in the JSON.
#     Return a structured JSON object with fields: source (Korba), destination (Delhi), date (2025-04-18), class (2A), trains (list of train details), and error (null or error message if applicable).
#     """

#     # Create and run the Agent
#     try:
#         agent = Agent(task=task, llm=llm, browser=browser)
#     except Exception as e:
#         print(f"Error initializing Agent: {str(e)}")
#         return {"source": "Korba", "destination": "Delhi", "date": "2025-04-18", "class": "2A", "trains": [], "error": f"Agent initialization failed: {str(e)}"}

#     # Run the agent and get results
#     try:
#         result = await agent.run()
#         print("Result:", result)
#         print("Result type:", type(result))
#         print("Result content:", [str(item) for item in result])  # Debug: Inspect AgentHistoryList
#     except Exception as e:
#         print(f"Error during agent execution: {str(e)}")
#         return {"source": "Korba", "destination": "Delhi", "date": "2025-04-18", "class": "2A", "trains": [], "error": f"Agent execution failed: {str(e)}"}

#     # Construct JSON output
#     json_output = {
#         "source": "Korba",
#         "destination": "Delhi",
#         "date": "2025-04-18",
#         "class": "2A",
#         "trains": [],
#         "error": None
#     }

#     # Process AgentHistoryList
#     try:
#         # Assume the final entry contains the JSON result
#         if result and isinstance(result, list) and len(result) > 0:
#             final_result = result[-1]  # Get the last entry
#             print("Final result:", final_result)

#             # Handle if final_result is a JSON string
#             if isinstance(final_result, str):
#                 try:
#                     final_result = json.loads(final_result)
#                 except json.JSONDecodeError as e:
#                     json_output["error"] = f"Failed to parse final result as JSON: {str(e)}"
#                     print(f"JSON parse error: {str(e)}")
#                     return json_output

#             # Handle if final_result is a dictionary
#             if isinstance(final_result, dict):
#                 trains = final_result.get("trains", [])
#                 if trains and isinstance(trains, list):
#                     json_output["trains"] = [
#                         {
#                             "train_number": train.get("train_number", "unknown"),
#                             "train_name": train.get("train_name", "unknown"),
#                             "departure": train.get("departure", "unknown"),
#                             "arrival": train.get("arrival", "unknown"),
#                             "duration": train.get("duration", "unknown"),
#                             "availability": train.get("availability", "unknown"),
#                             "fare": str(train.get("fare", "unknown"))
#                         }
#                         for train in trains
#                     ]
#                 json_output["error"] = final_result.get("error", None)
#             else:
#                 json_output["error"] = f"Unexpected final result type: {type(final_result)}"
#         else:
#             json_output["error"] = "No results returned by AgentHistoryList"
#     except Exception as e:
#         json_output["error"] = f"Error processing AgentHistoryList: {str(e)}"
#         print(f"Processing error: {str(e)}")

#     # Save JSON output to a file
#     output_file = "train_results.json"
#     try:
#         with open(output_file, "w") as f:
#             json.dump(json_output, f, indent=2)
#     except Exception as e:
#         print(f"Error saving JSON: {str(e)}")
#         json_output["error"] = f"{json_output.get('error', '')}; Failed to save JSON: {str(e)}"

#     # Print JSON output
#     print("\nResults:")
#     print(json.dumps(json_output, indent=2))

#     # List directory contents to locate trace/agent files
#     print("Directory contents:", os.listdir("."))

#     return json_output

# async def main():
#     """
#     Execute the railway agent to fetch train availability from Korba to Delhi.
#     """
#     print("🚆 Running Railway Booking Assistant with Browser Automation 🚆")
#     print("Fetching trains from Korba to Delhi on April 18, 2025, for 2A class...")
#     print("This may take a moment as the browser navigates to IRCTC...")
    
#     response = await railway_agent()
    
#     print("🚆 Search completed! 🚆")

# if __name__ == "__main__":
#     asyncio.run(main())



# import os
# import asyncio
# import json
# from dotenv import load_dotenv
# from browser_use import Agent, Browser
# from langchain_google_genai import ChatGoogleGenerativeAI
# from pydantic import SecretStr

# # Load environment variables
# load_dotenv()

# # Set Google API key (if needed, replace with your actual key or load from .env)
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "AIzaSyAHNTgXjpYON9rDBClw-SlugX1c1IGBdjo")

# async def railway_agent():
#     """
#     Railway agent to fetch train availability using browser automation.
#     """
#     result = {
#         "source": "Korba",
#         "destination": "Delhi",
#         "date": "2025-04-18",
#         "class": "2A",
#         "trains": [],
#         "error": None
#     }

#     # Define the task as a prompt
#     task = """
#     1. Navigate to https://www.irctc.co.in/nget/train-search.
#     2. In the 'From' field, type 'KORBA - KRBA' and select 'KORBA - KRBA (CHAMPA)' from the dropdown.
#     3. In the 'To' field, type 'DELHI - DLI' and select 'DELHI - DLI (NEW DELHI)' from the dropdown.
#     4. Select the journey date as '19-04-2025'.
#     5. Choose '2A (Second AC)' as the travel class.
#     6. Click the 'Search' button and wait for the train list to load.
#     6. Extract train details, including:
#        - train_number
#        - train_name
#        - departure
#        - arrival
#        - duration
#     Return the extracted train details in JSON format.
#     """

#     try:
#         # Initialize the browser
#         browser = Browser()

#         # Initialize the LLM
#         try:
#             api_key = os.environ["GOOGLE_API_KEY"]
#             llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(api_key))
#         except Exception as e:
#             print(f"Error initializing LLM: {str(e)}")
#             result["error"] = "LLM initialization failed. Please check your API key or quota."
#             return result

#         # Initialize the agent with the task, browser, and LLM
#         agent = Agent(task=task, browser=browser, llm=llm)

#         # Run the agent
#         result_data = await agent.run()

#         # Process the result
#         if isinstance(result_data, list):  # Check if result_data is a list (AgentHistoryList)
#             for action_result in result_data:
#                 if action_result.extracted_content:
#                     try:
#                         # Parse the extracted content as JSON
#                         extracted_data = json.loads(action_result.extracted_content)
#                         if "train_details" in extracted_data:  # Check for the correct key
#                             result["trains"].extend(extracted_data["train_details"])
#                     except json.JSONDecodeError:
#                         print(f"Invalid JSON in extracted content: {action_result.extracted_content}")
#                         continue
#         elif isinstance(result_data, str):  # Handle string result
#             try:
#                 extracted_data = json.loads(result_data)
#                 if "train_details" in extracted_data:  # Check for the correct key
#                     result["trains"] = extracted_data["train_details"]
#             except json.JSONDecodeError as e:
#                 result["error"] = f"Failed to parse result data: {str(e)}"

#     except Exception as e:
#         result["error"] = str(e)

#     # Save results to a JSON file
#     with open("train_results.json", "w") as f:
#         json.dump(result, f, indent=2)

#     # Print results
#     print(json.dumps(result, indent=2))

#     return result

# async def main():
#     """
#     Main function to execute the railway agent.
#     """
#     print("🚆 Fetching train details...")
#     response = await railway_agent()
#     print("🚆 Task completed!")
#     return response

# if __name__ == "__main__":
#     asyncio.run(main())




# import asyncio
# import os
# from browser_use import Controller, ActionResult
# from browser_use.agent.service import Agent
# from playwright.async_api import BrowserContext, Page
# from langchain_google_genai import ChatGoogleGenerativeAI
# from pydantic import BaseModel, SecretStr
# from typing import List
# import json


# # Define the output model for the Controller
# class TrainInfo(BaseModel):
#     train_number: str
#     train_name: str
#     departure: str
#     arrival: str
#     duration: str


# class TrainAvailability(BaseModel):
#     source: str
#     destination: str
#     date: str
#     trains: List[TrainInfo]


# # Initialize the Controller with the output model
# controller = Controller(output_model=TrainAvailability)


# @controller.action("Get Train Availability")
# async def get_attr_url(browser: BrowserContext) -> ActionResult:
#     """
#     Fetch train availability details.
    
#     Args:
#         browser: Playwright BrowserContext object
        
#     Returns:
#         ActionResult with TrainAvailability object
#     """
#     try:
#         # Get the current page from the browser context
#         if not browser.pages:
#             raise ValueError("No valid pages available in browser context")
#         page: Page = browser.pages[0]  # Assume first page is the active one
        
#         # Ensure page is loaded
#         for _ in range(3):
#             try:
#                 await page.goto("https://www.irctc.co.in/nget/train-search", timeout=60000)
#                 await page.wait_for_load_state("networkidle", timeout=60000)
#                 break
#             except Exception as e:
#                 print(f"Page load retry failed: {str(e)}")
#                 await asyncio.sleep(2)
        
#         # Wait for train list to load
#         await page.wait_for_selector(".train-list-row", timeout=60000)
        
#         # Get all train elements
#         train_elements = await page.query_selector_all(".train-list-row")
        
#         trains = []
#         for train in train_elements:
#             try:
#                 # Extract train details
#                 train_name_elem = await train.query_selector(".train-name")
#                 train_number_elem = await train.query_selector(".train-number")
#                 departure_elem = await train.query_selector(".departure-time")
#                 arrival_elem = await train.query_selector(".arrival-time")
#                 duration_elem = await train.query_selector(".duration")
                
#                 # Extract text or default to placeholders
#                 train_name = await train_name_elem.inner_text() if train_name_elem else "N/A"
#                 train_number = await train_number_elem.inner_text() if train_number_elem else "N/A"
#                 departure = await departure_elem.inner_text() if departure_elem else "N/A"
#                 arrival = await arrival_elem.inner_text() if arrival_elem else "N/A"
#                 duration = await duration_elem.inner_text() if duration_elem else "N/A"
                
#                 # Clean train_name
#                 if train_name and train_number and train_number in train_name:
#                     train_name = train_name.replace(f"({train_number})", "").strip()
                
#                 # Format duration (e.g., "32:17" → "32h 17m")
#                 if ":" in duration:
#                     hours, minutes = duration.split(":")
#                     duration = f"{hours}h {minutes}m"
                
#                 # Create TrainInfo object
#                 train_info = TrainInfo(
#                     train_number=train_number,
#                     train_name=train_name,
#                     departure=departure,
#                     arrival=arrival,
#                     duration=duration
#                 )
#                 trains.append(train_info)
#             except Exception as e:
#                 print(f"Error processing train: {str(e)}")
#                 continue
        
#         # Create TrainAvailability object
#         availability = TrainAvailability(
#             source="KORBA",
#             destination="DELHI",
#             date="2025-04-19",
#             trains=trains
#         )
        
#         return ActionResult(extractedContent={"availability": availability.dict()})
    
#     except Exception as e:
#         print(f"Error fetching train availability: {str(e)}")
#         return ActionResult(extractedContent={"availability": TrainAvailability(source="KORBA", destination="DELHI", date="2025-04-19", trains=[]).dict()})


# async def testValidation():
#     """
#     Test the railway agent to fetch train availability using a Controller.
#     """
#     # Set up the environment variable for the Google API key
#     os.environ["GOOGLE_API_KEY"] = "AIzaSyC2iA38riyH-CEK2nh_oR9YkyeHQ6uonBw"

#     # Define the task
#     task = (
#         """
#         1. Navigate to https://www.irctc.co.in/nget/train-search.
#         2. In the 'From' field, type 'KORBA - KRBA' and select 'KORBA - KRBA (CHAMPA)' from the dropdown.
#         3. In the 'To' field, type 'DELHI - DLI' and select 'DELHI - DLI (NEW DELHI)' from the dropdown.
#         4. Select the journey date as '19-04-2025'.
#         5. Click the class button with class 'ui-dropdown-trigger' and select '2A (Second AC)' from the listbox.
#         6. Click the 'Search' button and wait for the train list to load.
#         7. Fetch train availability details.
#         """
#     )

#     # Initialize the LLM
#     api_key = os.environ["GOOGLE_API_KEY"]
#     llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=SecretStr(api_key))

#     # Initialize the Agent with the task, controller, and LLM
#     agent = Agent(task=task, controller=controller, llm=llm)

#     # Run the Agent
#     history = await agent.run()
#     history.save_to_file("test_validation.json")

#     # Get the final result
#     test_result = history.final_result()
#     print("Test results:", test_result)
    
#     # Save the availability JSON to train_results.json
#     try:
#         # If final_result is None, try to get the last extracted content
#         if test_result is None:
#             # Look for the last extract_content action in history
#             for result in reversed(history.all_results):
#                 if result.extracted_content and isinstance(result.extracted_content, dict) and "availability" in result.extracted_content:
#                     result_data = result.extracted_content["availability"]
#                     break
#             else:
#                 result_data = {}
#         else:
#             result_data = test_result.extractedContent["availability"] if test_result.extractedContent else {}
        
#         with open("train_results.json", "w") as f:
#             json.dump(result_data, f, indent=2)
#         print("Fetched JSON saved to train_results.json")
#     except Exception as e:
#         print(f"Error saving to train_results.json: {str(e)}")


# # Run the testValidation function
# asyncio.run(testValidation())


# import asyncio
# import os
# from browser_use import Controller, ActionResult
# from browser_use.agent.service import Agent
# from playwright.async_api import BrowserContext, Page
# from langchain_google_genai import ChatGoogleGenerativeAI
# from pydantic import BaseModel, SecretStr
# from typing import List
# import json


# # Define the output model for the Controller
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


# # Initialize the Controller with the output model
# controller = Controller(output_model=TrainAvailability)


# @controller.action("Get Train Availability")
# async def get_attr_url(browser: BrowserContext) -> ActionResult:
#     """
#     Fetch train availability details.
    
#     Args:
#         browser: Playwright BrowserContext object
        
#     Returns:
#         ActionResult with TrainAvailability object
#     """
#     try:
#         # Get the current page from the browser context
#         if not browser.pages:
#             raise ValueError("No valid pages available in browser context")
#         page: Page = browser.pages[0]  # Assume first page is the active one
        
#         # Ensure page is loaded
#         for _ in range(3):
#             try:
#                 await page.goto("https://www.irctc.co.in/nget/train-search", timeout=60000)
#                 await page.wait_for_load_state("networkidle", timeout=60000)
#                 break
#             except Exception as e:
#                 print(f"Page load retry failed: {str(e)}")
#                 await asyncio.sleep(2)
        
#         # Wait for train list to load
#         await page.wait_for_selector(".train-list-row", timeout=60000)
        
#         # Dynamically fetch source, destination, and date
#         source_elem = await page.query_selector(".source-station")
#         destination_elem = await page.query_selector(".destination-station")
#         date_elem = await page.query_selector(".journey-date")
        
#         source = await source_elem.inner_text() if source_elem else " "
#         destination = await destination_elem.inner_text() if destination_elem else " "
#         date = await date_elem.inner_text() if date_elem else ""
        
#         # Clean extracted values if necessary
#         source = source.strip() if source else ""
#         destination = destination.strip() if destination else ""
#         date = date.strip() if date else " "
        
#         # Get all train elements
#         train_elements = await page.query_selector_all(".train-list-row")
        
#         trains = []
#         for train in train_elements:
#             try:
#                 # Select 2A class for the train (Step 7)
#                 await train.click('button:has-text("2A")', timeout=5000)
#                 await page.wait_for_timeout(1000)  # Wait for availability to load
                
#                 # Extract train details
#                 train_name_elem = await train.query_selector(".train-name")
#                 train_number_elem = await train.query_selector(".train-number")
#                 departure_elem = await train.query_selector(".departure-time")
#                 arrival_elem = await train.query_selector(".arrival-time")
#                 duration_elem = await train.query_selector(".duration")
#                 fare_elem = await train.query_selector(".fare")  # Added fare selector
                
#                 # Extract text or default to placeholders
#                 train_name = await train_name_elem.inner_text() if train_name_elem else "N/A"
#                 train_number = await train_number_elem.inner_text() if train_number_elem else "N/A"
#                 departure = await departure_elem.inner_text() if departure_elem else "N/A"
#                 arrival = await arrival_elem.inner_text() if arrival_elem else "N/A"
#                 duration = await duration_elem.inner_text() if duration_elem else "N/A"
#                 fare = await fare_elem.inner_text() if fare_elem else "N/A"  # Extract fare
                
#                 # Clean train_name
#                 if train_name and train_number and train_number in train_name:
#                     train_name = train_name.replace(f"({train_number})", "").strip()
                
#                 # Format duration (e.g., "32:17" → "32h 17m")
#                 if ":" in duration:
#                     hours, minutes = duration.split(":")
#                     duration = f"{hours}h {minutes}m"
                
#                 # Create TrainInfo object
#                 train_info = TrainInfo(
#                     train_number=train_number,
#                     train_name=train_name,
#                     departure=departure,
#                     arrival=arrival,
#                     duration=duration,
#                     fare=fare  # Include fare
#                 )
#                 trains.append(train_info)
                
#                 # Scroll to ensure all trains are processed
#                 await train.scroll_into_view_if_needed()
#             except Exception as e:
#                 print(f"Error processing train: {str(e)}")
#                 continue
        
#         # Create TrainAvailability object with dynamic values
#         availability = TrainAvailability(
#             source=source,
#             destination=destination,
#             date=date,
#             trains=trains
#         )
        
#         return ActionResult(extractedContent={"availability": availability.dict()})
    
#     except Exception as e:
#         print(f"Error fetching train availability: {str(e)}")
#         return ActionResult(extractedContent={"availability": TrainAvailability(source=source, destination=destination, date=date, trains=[]).dict()})


# async def testValidation():
#     """
#     Test the railway agent to fetch train availability using a Controller.
#     """
#     # Set up the environment variable for the Google API key
#     os.environ["GOOGLE_API_KEY"] = "AIzaSyC2iA38riyH-CEK2nh_oR9YkyeHQ6uonBw"

#     # Define the task
#     task = (
#         """
#         1. Navigate to https://www.irctc.co.in/nget/train-search.
#         2. In the 'From' field, type 'KORBA - KRBA' and select 'KORBA - KRBA (CHAMPA)' from the dropdown.
#         3. In the 'To' field, type 'DELHI - DLI' and select 'DELHI - DLI (NEW DELHI)' from the dropdown.
#         4. Select the journey date as '19-04-2025'.
#         5. Select 2A class from class dropdown.
#         6. Click the 'Search' button and wait for the train list to load.
#         7. Click 2A for all trains displayed on the page.
#         8. Fetch train availability details.
#         """
#     )

#     # Initialize the LLM
#     api_key = os.environ["GOOGLE_API_KEY"]
#     llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=SecretStr(api_key))

#     # Initialize the Agent with the task, controller, and LLM
#     agent = Agent(task=task, controller=controller, llm=llm)

#     # Run the Agent
#     history = await agent.run()
#     history.save_to_file("test_validation.json")

#     # Get the final result
#     test_result = history.final_result()
#     print("Test results:", test_result)
    
#     # Save the entire test_result JSON to train_results.json
#     try:
#         # If test_result is None, try to get the last extracted content
#         if test_result is None:
#             # Look for the last extract_content action in history
#             for result in reversed(history.all_results):
#                 if result.extracted_content:
#                     test_result = result.extracted_content
#                     break
#             else:
#                 test_result = {}

#         # If test_result is a string, parse it as JSON
#         if isinstance(test_result, str):
#             try:
#                 test_result = json.loads(test_result)
#             except json.JSONDecodeError:
#                 print("Error: test_result is not valid JSON.")
#                 test_result = {}

#         # Save the entire test_result to train_results.json
#         with open("train_results.json", "w") as f:
#             json.dump(test_result, f, indent=2)
#         print("Fetched JSON saved to train_results.json")
#     except Exception as e:
#         print(f"Error saving to train_results.json: {str(e)}")


# # Run the testValidation function
# asyncio.run(testValidation())


# import asyncio
# import os
# from browser_use import Controller, ActionResult
# from browser_use.agent.service import Agent
# from playwright.async_api import BrowserContext, Page
# from langchain_google_genai import ChatGoogleGenerativeAI
# from pydantic import BaseModel, SecretStr
# from typing import List
# import json


# # Define the output model for the Controller
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


# # Initialize the Controller with the output model
# controller = Controller(output_model=TrainAvailability)


# async def testValidation():
#     """
#     Test the railway agent to fetch train availability using a Controller.
#     """
#     # Set up the environment variable for the Google API key
#     os.environ["GOOGLE_API_KEY"] = "AIzaSyC2iA38riyH-CEK2nh_oR9YkyeHQ6uonBw"

#    # Define the task
#     task = (
#         """
#         1. Open the IRCTC train search page: https://www.irctc.co.in/nget/train-search.
#         2. In the 'From' field, type 'Bangalore' and select 'KSR BENGALURU - SBC' from the dropdown.
#         3. In the 'To' field, type 'DELHI - DLI' and select 'DELHI - DLI (NEW DELHI)' from the dropdown.
#         4. Set the journey date to '20-04-2025'.
#         5. Choose '2A' class from the dropdown menu.
#         6. Click the 'Search' button and wait for the train list to load (timeout: 5 seconds).
#         7. Perform the following actions:
#              a. Wait for the train list container to become visible (timeout: 3 seconds).
#              b. Locate the '2A' seat cell and Click the '2A' button. (timeout: 2 seconds).
#              c. Scroll through the train list container, wait for '2A' button to be displayed and click '2A' button for train until Fare amount is visible. (timelimit: 5 seconds).
#              d. Wait for step 7 to complete, Extract details Return the train availability details in JSON format using the TrainAvailability model. (timelimit: 5 seconds).
     
#         """
#     )

#     # Initialize the LLM
#     api_key = os.environ["GOOGLE_API_KEY"]
#     llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=SecretStr(api_key))

#     # Initialize the Agent with the task, controller, and LLM
#     agent = Agent(task=task, controller=controller, llm=llm)

#     # Run the Agent
#     history = await agent.run()
#     history.save_to_file("test_validation.json")

#     # Get the final result
#     test_result = history.final_result()
#     print("Test results:", test_result)
    
#     # Save the test results to train_results.json
#     with open("train_results.json", "w") as f:
#         json.dump(test_result, f, indent=2)

# # Run the testValidation function
# asyncio.run(testValidation())


# import asyncio
# import os
# import json
# from datetime import datetime, timedelta
# from browser_use import Controller, Agent
# from langchain_google_genai import ChatGoogleGenerativeAI
# from pydantic import BaseModel, SecretStr
# from typing import List


# # Define the output model for the Controller
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


# # Initialize the Controller with the output model
# controller = Controller(output_model=TrainAvailability)


# async def railway_agent(user_query: str):
#     """
#     Railway agent that uses browser automation to check train availability.
#     Args:
#         user_query: Natural language query about train availability.
#     """
#     # Extract travel parameters from the user query
#     print("\nProcessing your query...")
#     source = input("Enter source station: ")
#     destination = input("Enter destination station: ")
#     travel_date = input("Enter travel date (YYYY-MM-DD): ")
#     travel_class = input("Enter travel class (e.g., 3AC, 2AC): ")

#     # Define the task
#     task = f"""
#     1. Open the IRCTC train search page: https://www.irctc.co.in/nget/train-search.
#     2. In the 'From' field, type '{source}' and select the appropriate station from the dropdown.
#     3. In the 'To' field, type '{destination}' and select the appropriate station from the dropdown.
#     4. Set the journey date to '{travel_date}'.
#     5. Choose '{travel_class}' class from the dropdown menu.
#     6. Click the 'Search' button and wait for the train list to load (timeout: 5 seconds).
#     7. Extract details and return the train availability details in JSON format using the TrainAvailability model. Ensure the output is a valid JSON object — do not escape it or wrap it in quotes (timelimit: 15 seconds).
#     """

#     # Initialize the LLM
#     api_key = os.environ.get("GOOGLE_API_KEY", "your-google-api-key")
#     llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=SecretStr(api_key))

#     # Initialize the Agent with the task, controller, and LLM
#     agent = Agent(task=task, controller=controller, llm=llm)

#     # Run the Agent
#     history = await agent.run()
#     history.save_to_file("test_validation.json")

#     # Get the final result
#     test_result = history.final_result()
#     print("\nTest results:", test_result)

#     # Save the test results to train_results.json
#     try:
#         data = json.loads(test_result)
#     except json.JSONDecodeError:
#         print("Error: test_result is not valid JSON.")
#         return

#     # Save the parsed results to train_results.json
#     with open("train_results.json", "w") as f:
#         json.dump(data, f, indent=4)

#     print("\nResults saved to train_results.json")


# async def main():
#     print("🚆 Welcome to the Railway Booking Assistant 🚆")
#     print("I can help you find train availability between cities in India.")
#     print("Type 'exit' to quit.")

#     while True:
#         user_query = input("\nWhat would you like to know about train availability? (or 'exit' to quit): ")
#         if user_query.lower() in ["exit", "quit", "bye"]:
#             print("Thank you for using the Railway Booking Assistant. Happy travels! 👋")
#             break

#         await railway_agent(user_query)


# # Run the main function
# if __name__ == "__main__":
#     asyncio.run(main())

Find trains from Mysuru to Delhi for 2025-04-22 for 1A class