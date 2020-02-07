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
    result: Dict[str, str] = dict()
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
            break
        key = pair[0][0]
        value = pair[0][1]
        result[key] = value
        pairs[i] = pair[0]  # pair это [(k,v)]
        i = i + 1
    return result


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

def get_person_for_insert(text: str) -> Person


def get_person_from_text(text: str) -> Person:
    if len(text) == 0:
        return None
    line = clean_str(text)
    data = str_to_dict(text)
    if len(data) < 1:
        return None
    if ('id' not in data) and ('name' not in data):
        return None
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


def create_persons_from_mail_data(data: str) -> List[Person]:
    persons = list()
    lines = data.split('\n')
    for line in lines:
        if line == "":
            continue
        person: Person = get_person_from_text(line)
        if person is not None:
            persons.append(person)
    return persons
