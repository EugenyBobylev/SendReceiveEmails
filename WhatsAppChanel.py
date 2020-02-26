import requests
import json


# chat2desk api info
def get_info() -> object:
    url = "https://api.chat2desk.com/v1/companies/api_info"
    payload = {}
    headers = {'Authorization': '456c1286ccf71bfcd1bda342d92a70'}

    response = requests.request("GET", url, headers=headers, data=payload)
    __data__ = json.load(response) if response.ok else None
    return __data__


# chat2desk api modes
def get_api_modes() -> object:
    url = "https://api.chat2desk.com/v1/companies/api_modes"
    payload = {}
    headers = {'Authorization': '456c1286ccf71bfcd1bda342d92a70'}

    response = requests.request("GET", url, headers=headers, data=payload)
    __data__ = json.load(response) if response.ok else None
    return __data__


# load api info json from file
def load_data_json():
    __data__ = None
    with open('c:/Users/Bobylev/My Documents/data.json', mode='r', encoding='utf-8') as f:
        __data__ = json.load(f)
    return __data__


api_modes = get_api_modes()
print(api_modes)
