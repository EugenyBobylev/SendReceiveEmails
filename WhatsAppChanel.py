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
    url = "https://api.chat2desk.com/v1/help/api_modes"
    payload = {}
    headers = {'Authorization': token}

    response = requests.request("GET", url, headers=headers, data=payload)
    __data__ = json.loads(response.text) if response.ok else None
    return __data__


# chat2client api transports (Get)
def get_api_transports() -> object:
    url = "https://api.chat2desk.com/v1/help/transports"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    __data__ = json.loads(response.text) if response.ok else None
    return __data__


# chat2desk api channels (GET)
def get_api_channels() -> object:
    url = "https://api.chat2desk.com/v1/channels"
    payload = {}
    headers = {'Authorization': token}

    response = requests.request("GET", url, headers=headers, data=payload)
    __data__ = json.loads(response.text) if response.ok else None
    return __data__


# chat2client api clients (GET)
def get_api_clients() -> object:
    url = "https://api.chat2desk.com/v1/clients"
    payload = {}
    headers = {'Authorization': token}

    response = requests.request("GET", url, headers=headers, data=payload)
    __data__ = json.loads(response.text) if response.ok else None
    return __data__

# chat2desk api create new client (POST)
def post_api_client() -> object:
    url = "https://api.chat2desk.com/v1/clients"

    payload = '{\n\t"phone":79247401790,\n\t"transport":"viber_public"\n\t,"nickname":"EugenyBobylev"\n}'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'charset': 'UTF-8'
    }

    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
    __data__ = json.loads(response.text)
    return __data__


# chat2desk change of clint
def put_api_clients(client_id) -> object:
    url = f"https://api.chat2desk.com/v1/clients/{client_id}"

    payload = '{\n\t"nickname": "BobylevEA"\n}'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'charset': 'UTF-8'
    }

    response = requests.request("PUT", url, headers=headers, data=payload.encode('utf-8'))
    __data__ = json.loads(response.text)
    return __data__


# load api info json from file
def load_data_json():
    __data__ = None
    with open('c:/Users/Bobylev/My Documents/data.json', mode='r', encoding='utf-8') as f:
        __data__ = json.load(f)
    return __data__


data = None
# data = get_api_modes()
#data = get_api_transports()
#data = get_api_clients()
# data = get_api_channels()
# data = post_api_client()
# data = put_api_clients(client_id=96881373)
print(data)
