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


def prepare_person_data(data_dict: Dict[str, str]) -> Dict[str, object]:
    for key, val in data_dict.items():
        if val in ["None", "none", ""]:
            data_dict[key] = None
        if key == 'id' and val is not None:
            data_dict[key] = str_to_int(val)
        if key == 'is_customer':
            data_dict[key] = val in ["True", "true", "1", "Да", "да"]
        if key == 'is_performer':
            data_dict[key] = val in ["True", "true", "1", "Да", "да"]
    return data_dict


def create_person_data_from_string(text: str) -> Dict[str, object]:
    if len(text) == 0:
        return None
    line = clean_str(text)
    data = str_to_dict(line)
    if len(data) < 1:   # пустой словарь
        return None
    data = prepare_person_data(data)
    return data


def create_persons_data_from_string(text: str) -> List[Dict]:
    lines = split_input_text(text)
    persons_data = list()
    for line in lines:
        person_data = create_person_data_from_string(line)
        if person_data is not None:
            persons_data.append(person_data)
    return persons_data


def create_person_from_data(person_data) -> Person:
    person = Person()
    for key in person_data:
        if hasattr(person, key):
            value = person_data[key]
            setattr(person, key, value)
    return person


def create_person_from_string(text: str) -> Person:
    data = create_person_data_from_string(text)
    if data is None:
        return None
    person = create_person_from_data(data)
    if not person.is_performer and not person.is_performer:
        person.is_customer = True
    return person


def split_input_text(txt: str) -> List[str]:
    strings = txt.split('\n')
    i = 0
    while i < len(strings):  # delete empty strings
        if strings[i].strip() == "":
            strings.remove(strings[i])
            continue
        i += 1
    return strings


def create_persons_from_mail_data(text: str) -> List[Person]:
    persons = list()
    persons_data = create_persons_data_from_string(text)
    for person_data in persons_data:
        person: Person = create_person_from_data(person_data)
        if not person.is_performer and not person.is_performer:
            person.is_customer = True
        if person is not None:
            persons.append(person)
    return persons
