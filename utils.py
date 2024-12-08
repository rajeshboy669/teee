import json
import re
import requests

# File for storing user data
USER_DATA_FILE = "user_data.json"

def load_user_data():
    """Load user data from file."""
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    """Save user data to file."""
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def extract_links(text):
    """Extract all links from a given text."""
    return re.findall(r'(https?://[^\s]+|\bwww\.[^\s]+)', text)

def shorten_url(api_key, url, alias=None):
    """Shorten a URL using the API."""
    api_url = f"{DEFAULT_API_URL}?api={api_key}&url={url}"
    if alias:
        api_url += f"&alias={alias}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
