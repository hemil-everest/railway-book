import asyncio
import json
import requests
import logging
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('irctc_agent_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Query Ollama's DeepSeek model
def query_ollama(prompt: str, model: str = "deepseek-r1:8b") -> str:
    base_url = "http://localhost:11434/api/chat"
    try:
        response = requests.post(
            base_url,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "options": {"seed": 101, "temperature": 0}
            },
            stream=True,
            timeout=30
        )
        if response.status_code == 200:
            message = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        content = data.get("message", {}).get("content", "")
                        message += content
                    except json.JSONDecodeError:
                        logger.error(f"Failed to decode line: {line}")
            logger.debug(f"Ollama response: {message}")
            return message.strip()
        else:
            logger.error(f"Ollama request failed: {response.text}")
            return ""
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        return ""

# Simple Playwright Agent
async def deepseek_agent(task: str):
    prompt = (
        f"Task: {task}\n\n"
        f"Website: https://www.irctc.co.in/nget/train-search\n\n"
        f"Generate a sequence of Playwright actions to complete the task. "
        f"Return a JSON object with an 'actions' array, where each action has: "
        f"'instruction' (description), 'action' (e.g., 'fill', 'click', 'select_option', 'extract'), "
        f"'selector' (XPath selector), and 'value' (value to use, if applicable). "
        f"For the From field, use selector //*[@id=\"origin\"]/span/input, fill with 'Delhi', wait 1 second, and press Enter to select the autocomplete suggestion. "
        f"For the To field, use selector //*[@id=\"destination\"]/span/input, fill with 'Jaipur', wait 1 second, and press Enter. "
        f"Set date to '20-04-2025' using selector //*[@id=\"jDate\"]/span/input. "
        f"Select '2A' class using selector //select[contains(@class, 'form-control')]. "
        f"Click the search button using selector //button[@label='Find Trains']. "
        f"Extract train data using 'action': 'extract' with a 'data' array of trains including "
        f"'train_name', 'train_number', 'departure', 'arrival', 'availability'. "
        f"Click 'Book Now' using selector //button[contains(@data-train-number, '')]. "
        f"Include a 'queries' array answering: "
        f"1. List all trains with departure and arrival times. "
        f"2. Earliest departure train. "
        f"3. Any train with available 2A seats. "
        f"Example: "
        f"{{\"actions\": [{{\"instruction\": \"Fill From\", \"action\": \"fill\", \"selector\": \"//*[@id=\\\"origin\\\"]/span/input\", \"value\": \"Delhi\"}}], "
        f"\"queries\": [{{\"query\": \"List trains\", \"response\": \"...\"}}]}}"
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        result = {"task": task, "status": "Failed", "details": "", "query_results": []}

        try:
            # Navigate to IRCTC
            logger.info("Navigating to IRCTC...")
            await page.goto("https://www.irctc.co.in/nget/train-search", timeout=60000)
            await page.wait_for_load_state("domcontentloaded", timeout=60000)
            logger.info("Page loaded.")

            # Query DeepSeek
            logger.info("Querying DeepSeek...")
            response = query_ollama(prompt)
            logger.debug(f"DeepSeek response: {response}")
            if not response:
                result["details"] = "Empty response from DeepSeek."
                return result

            # Parse actions and queries
            try:
                data = json.loads(response)
                actions = data.get("actions", [])
                query_results = data.get("queries", [])
                logger.info(f"Parsed {len(actions)} actions and {len(query_results)} query results.")
            except json.JSONDecodeError:
                result["details"] = f"Invalid JSON from DeepSeek: {response}"
                return result

            # Execute actions
            for action_data in actions:
                instruction = action_data.get("instruction", "")
                action = action_data.get("action", "none")
                selector = action_data.get("selector", "")
                value = action_data.get("value", "")

                logger.info(f"Executing: {instruction}")

                try:
                    if action == "fill":
                        await page.fill(selector, value)
                        logger.info(f"Filled {selector} with {value}")
                        if "From" in instruction or "To" in instruction:
                            await page.wait_for_timeout(1000)
                            await page.press(selector, "Enter")
                            logger.info(f"Pressed Enter on {selector}")
                    elif action == "click":
                        await page.click(selector)
                        logger.info(f"Clicked {selector}")
                    elif action == "select_option":
                        await page.select_option(selector, value=value)
                        logger.info(f"Selected {value} in {selector}")
                    elif action == "extract":
                        result["train_data"] = action_data.get("data", [])
                        logger.info(f"Extracted {len(result['train_data'])} trains")
                    else:
                        logger.warning(f"Unsupported action: {action}")
                        continue

                    # Check for CAPTCHA
                    if "search" in instruction.lower() or "book" in instruction.lower():
                        captcha = await page.query_selector('img[src*="captcha"]')
                        if captcha:
                            logger.warning("CAPTCHA detected.")
                            print("CAPTCHA detected. Solve it in the browser and press Enter in the terminal.")
                            input("Solve the CAPTCHA and press Enter...")
                            logger.info("CAPTCHA solved.")

                    await page.wait_for_load_state("networkidle", timeout=60000)

                except PlaywrightTimeoutError as e:
                    logger.error(f"Playwright TimeoutError for action '{instruction}' with selector '{selector}': {e}")
                    print(f"Playwright Error: TimeoutError - Action '{instruction}' failed: {e}")
                    result["details"] = f"TimeoutError for {instruction}: {e}"
                    return result
                except PlaywrightError as e:  # Fixed syntax here
                    logger.error(f"Playwright Error for action '{instruction}' with selector '{selector}': {e}")
                    print(f"Playwright Error: {e}")
                    result["details"] = f"Error for {instruction}: {e}"
                    return result

            result["status"] = "Success"
            result["details"] = f"Completed task. Extracted {len(result.get('train_data', []))} trains."
            result["query_results"] = [
                {"query": q["query"], "response": q["response"]}
                for q in query_results
            ]

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"Unexpected Error: {e}")
            result["details"] = str(e)
        finally:
            await browser.close()
            return result

# Main function
async def main():
    print("🚆 Railway Booking Assistant 🚆")
    print("Enter a task like: 'Book tickets from Delhi to Jaipur for 2A class on 2025-04-20'")
    print("Type 'exit' to quit.")

    while True:
        task = input("\nTask (or 'exit'): ")
        if task.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        task = f"{task}. Use the IRCTC website (https://www.irctc.co.in/nget/) to complete this task."
        print("Processing...")
        response = await deepseek_agent(task)
        print("\nResults:")
        print(json.dumps(response, indent=2))

if __name__ == "__main__":
    asyncio.run(main())