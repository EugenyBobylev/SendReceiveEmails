import requests
import json
from pathlib import Path


# chat2desk api info
def get_info() -> None:
    url = "https://api.chat2desk.com/v1/companies/api_info"
    payload = {}
    headers = {'Authorization': '456c1286ccf71bfcd1bda342d92a70'}

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)


data = None
with open('c:/Users/Bobylev/My Documents/data.json', mode='r', encoding='utf-8') as f:
    data = json.load(f)
print(data)
