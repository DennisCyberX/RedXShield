import requests
import os

API_KEY = os.getenv("VT_API_KEY")
BASE_URL = "https://www.virustotal.com/api/v3/urls"

def scan_url(url):
    headers = {"x-apikey": API_KEY}
    response = requests.post(BASE_URL, headers=headers, data={"url": url})
    return response.json()
