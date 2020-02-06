from typing import Dict, List
import re
from models import Person

def str_to_dict(data_str: str) -> Dict:
    pairs = re.findall("(.*?)(?:,|;|$)", data_str)
    for i in range(len(pairs)):
        if pairs[i] == '':
            pairs.remove(pairs[i])
            continue
        pair = pairs[i]
        pair = re.findall("\\s*(.*?)\\s*[:|=]\\s*(.*)\\s*", pair)
        pairs[i] = pair[0]  # pair это [(k,v)]
    d: Dict = {k.lower(): v for (k, v) in pairs}
    return d


def parse(key: str):
    if key in data:
        return data[key]
    else:
        return None


def str_to_int(value: str):
    if value is None:
        return None
    result = None
    try:
        result = int(value)
    except ValueError:
        pass
    return result


def clean_str(value: str) -> str:
    value = value.replace("\"", "")
    value = value.replace("'","")
    value = value.replace("&quot;", "")
    return value


def parse_mail(line: str) -> Dict:
    line = clean_str(line)
    data = str_to_dict(line)
    person = Person()
    person.id = str_to_int(parse('id'))
    person.name = parse('name')
    person.email = parse('email')
    person.phone = parse('phone')
    person.is_customer = parse('is_customer') == 'True'
    person.is_performer = parse('is_performer') == 'True'

str1 = "email: ohmanyukov@mail.ru, Id: None, is_customer: True, is_performer: None, Name: Ольга Охманюк, phone: '+79246432292'"
str2 = "name=\"Бобылев Евгений\"; phone=+79247401790; email=gomirka@mail.ru; is_customer=True"

line = clean_str(str2)
result = str_to_dict(line)
print(result)
