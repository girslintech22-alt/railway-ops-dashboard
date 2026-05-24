import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAILRADAR_API_KEY")

print("API KEY:", API_KEY)

headers = {
    "X-API-Key": API_KEY
}

url = "https://api.railradar.org/api/v1/trains/12951"

try:
    response = requests.get(url, headers=headers, timeout=15)

    print("STATUS:", response.status_code)
    print(response.text[:300])

except Exception as e:
    print("ERROR:", e)