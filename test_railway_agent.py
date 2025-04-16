import pytest
import asyncio
from railway_agent_browser import railway_agent

def run_async_test(query: str):
    return asyncio.run(railway_agent(query))

def test_basic_query_structure():
    response = run_async_test("Find trains from Delhi to Mumbai")
    required_keys = ["source", "destination", "date", "class", "trains"]
    for key in required_keys:
        assert key in response

def test_class_extraction():
    response = run_async_test("Trains from Chennai to Bangalore in sleeper class")
    assert response["class"] == "sleeper"

def test_no_trains_route():
    response = run_async_test("Any trains between Delhi and Leh?")
    assert response["source"] == "Delhi"
    assert response["destination"] == "Leh"
    assert isinstance(response["trains"], list)

def test_date_extraction():
    response = run_async_test("Trains from Mumbai to Pune on Friday")
    assert "date" in response

def test_train_structure():
    response = run_async_test("Trains from Delhi to Mumbai")
    if not response.get("trains"):
        pytest.skip("No trains found")
    train = response["trains"][0]
    for key in ["train_number", "train_name", "departure", "arrival", "duration", "availability", "fare"]:
        assert key in train