import requests
import json
token = '456c1286ccf71bfcd1bda342d92a70'


# chat2desk api info
def get_info() -> object:
    url = "https://api.chat2desk.com/v1/companies/api_info"
    payload = {}
    headers = {'Authorization': token}

    response = requests.request("GET", url, headers=headers, data=payload)
    __data__ = json.loads(response.text) if response.ok else None
    return __data__


# chat2desk api modes
def get_api_modes() -> object:
    url = "https://api.chat2desk.com/v1/companies/api_modes"
    payload = {}
    headers = {'Authorization': token}

    response = requests.request("GET", url, headers=headers, data=payload)
    __data__ = json.loads(response.text) if response.ok else None
    return __data__


# chat2desk api channels (GET)
def get_api_channels(phone) -> object:
    url = f"https://api.chat2desk.com/v1/channels?phone={phone}"
    payload = {}
    headers = {'Authorization': token}

    response = requests.request("GET", url, headers=headers, data=payload)
    __data__ = json.loads(response.text) if response.ok else None
    return __data__


# load api info json from file
def load_data_json():
    __data__ = None
    with open('c:/Users/Bobylev/My Documents/data.json', mode='r', encoding='utf-8') as f:
        __data__ = json.load(f)
    return __data__


data = get_api_channels('79247401790')
print(data)
