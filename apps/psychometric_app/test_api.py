import requests
import json

url = 'http://127.0.0.1:8000/api/career-advice/'

payload = {
    "topic": "personality",
    "performance_data": [
        {"question": "I like parties", "selected_option": "Agree", "correct": True, "topic_category": "Extroversion"},
        {"question": "I pay attention to detail", "selected_option": "Agree", "correct": True, "topic_category": "Conscientiousness"},
        {"question": "I get stressed easily", "selected_option": "Disagree", "correct": True, "topic_category": "Neuroticism"}
    ]
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Raw Content: {response.text}")
    try:
        print(f"JSON: {response.json()}")
    except:
        print("Not valid JSON")
except Exception as e:
    print(f"Request Error: {e}")
