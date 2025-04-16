# test_weather_ollama.py
import requests
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama


def get_weather(city: str) -> str:
    """
    Get current weather for a city using wttr.in (no API key required).
    Returns plain text.
    """
    try:
        url = f"http://wttr.in/{city}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return "Unable to fetch weather data."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

def ask_llama_about_weather(city: str):
    weather_info = get_weather(city)

    llm = ChatOllama(model="llama3")

    prompt = f"The current weather in {city} is:\n{weather_info}\n\n"
    prompt += "Based on this, how would you describe the weather to a traveler?"

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content


if __name__ == "__main__":
    city = input("Enter a city name to get the weather: ")
    answer = ask_llama_about_weather(city)
    print("\n--- LLaMA's Response ---")
    print(answer)