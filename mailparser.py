import base64
from email import encoders
from typing import Dict, List
import re
from models import Person

def clean_str(value: str) -> str:
    value = value.replace("\"", "")
    value = value.replace("'","")
    value = value.replace("&quot;", "")
    value = value.replace("&#39;", "")
    return value


def str_to_dict(data_str: str) -> Dict[str, str]:
    pairs = re.findall("(.*?)(?:,|;|$)", data_str, flags=re.MULTILINE)
    i = 0
    while i < len(pairs):
        if pairs[i] == '':
            pairs.remove(pairs[i])
            continue
        pair = pairs[i]
        pair = re.findall("\\s*(.*?)\\s*[:|=]\\s*(.*)\\s*", pair)
        if len(pair) == 0:
            pairs.remove(pairs[i])
            return None
        pairs[i] = pair[0]  # pair это [(k,v)]
        i = i + 1
    d: Dict = {k.lower(): v for (k, v) in pairs}
    return d


def str_to_int(value: str):
    result = None
    try:
        result = int(value)
    except ValueError:
        pass
    return result


def prepare_person_data(dict: Dict[str, str]) -> Dict[str, object]:
    for key, val in dict.items():
        if val in ["None", "none", ""]:
            dict[key] = None
        if key == 'id' and val is not None:
            dict[key] = str_to_int(val)
        if key == 'is_customer':
            dict[key] = val in ["True", "true", "1", "Да", "да"]
        if key == 'is_performer':
            dict[key] = val in ["True", "true", "1", "Да", "да"]
    return dict


def get_person_from_mail(line: str) -> Person:
    person: Person = None
    if len(line) == 0:
        return person
    line = clean_str(line)
    data = str_to_dict(line)
    if data is not None:
        data = prepare_person_data(data)
        person = Person()
        person.id = data['id'] if 'id' in data else None
        person.name = data['name']
        person.email = data['email'] if 'email' in data else ''
        person.phone = data['phone'] if 'phone' in data else ''
        person.is_performer = data['is_performer'] if 'is_performer' in data else False
        person.is_customer = data['is_customer'] if 'is_customer' in data else False
        if not person.is_performer and not person.is_performer:
            person.is_customer = True
    return person

#str1 = "email: ohmanyukov@mail.ru, Id: 1234, is_customer: True, is_performer: none, Name: Ольга Охманюк, phone: '+79246432292'"
#str2 = "name=\"Бобылев Евгений\"; phone=+79247401790; email=gomirka@mail.ru; is_customer=True"
#str3 = "'email: ohmanyukov@mail.ru, id: None, is_customer: True, is_performer: None, name: Ольга Охманюк, phone: &#39;+79246432292&#39; -- Eugeny Bobylev'"
#str4 = "'CmVtYWlsOiAgb2htYW55dWtvdkBtYWlsLnJ1ICwgaWQ6IE5vbmUsIGlzX2N1c3RvbWVyOiBUcnVlLCBpc19wZXJmb3JtZXI6IE5vbmUsIG5hbWU6INCe0LvRjNCz0LAg0J7RhdC80LDQvdGO0LosIHBob25lOiAnKzc5MjQ2NDMyMjkyJwrCoAotLQpFdWdlbnkgQm9ieWxldg=='"
#decoded_bytes = base64.standard_b64decode(str4)
#decoded_str = decoded_bytes.decode('utf-8')
#print(decoded_str)

str5 = """

email:  ohmanyukov@mail.ru , id: None, is_customer: True, is_performer: None, name: Ольга Охманюк, phone: '+79246432292'
 
--
Eugeny Bobylev
"""
lines = str5.split('\n')
for line in lines:
    person: Person = get_person_from_mail(line)
    print(person)
#person2 = get_person_from_mail(str2)
#print(person2)

