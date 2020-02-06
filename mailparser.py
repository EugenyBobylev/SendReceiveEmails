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


def get_person_from_text(text: str) -> Person:
    if len(text) == 0:
        return None
    line = clean_str(text)
    data = str_to_dict(text)
    if data is None:
        return None
    if 'name' not in data:
        return None
    if 'email' not in data:
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


def create_persons_from_mail_data(data: str)-> List[Person]:
    persons = list()
    lines = data.split('\n')
    for line in lines:
        if line == "":
            continue
        person: Person = get_person_from_text(line)
        if person is not None:
            persons.append(person)
    return persons

#str1 = "email: ohmanyukov@mail.ru, Id: 1234, is_customer: True, is_performer: none, Name: Ольга Охманюк, phone: '+79246432292'"
#str2 = "name=\"Бобылев Евгений\"; phone=+79247401790; email=gomirka@mail.ru; is_customer=True"
#str3 = "'email: ohmanyukov@mail.ru, id: None, is_customer: True, is_performer: None, name: Ольга Охманюк, phone: &#39;+79246432292&#39; -- Eugeny Bobylev'"
#str4 = "'CmVtYWlsOiAgb2htYW55dWtvdkBtYWlsLnJ1ICwgaWQ6IE5vbmUsIGlzX2N1c3RvbWVyOiBUcnVlLCBpc19wZXJmb3JtZXI6IE5vbmUsIG5hbWU6INCe0LvRjNCz0LAg0J7RhdC80LDQvdGO0LosIHBob25lOiAnKzc5MjQ2NDMyMjkyJwrCoAotLQpFdWdlbnkgQm9ieWxldg=='"
#str6 = "PGRpdj48ZGl2IHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOnJnYiggMjU1ICwgMjU1ICwgMjU1ICk7Y29sb3I6cmdiKCAzNCAsIDM0ICwgMzQgKTtmb250LWZhbWlseTonYXJpYWwnICwgJ2hlbHZldGljYScgLCBzYW5zLXNlcmlmO2ZvbnQtc2l6ZTpzbWFsbDtmb250LXN0eWxlOm5vcm1hbDtmb250LXdlaWdodDo0MDA7dGV4dC1kZWNvcmF0aW9uLXN0eWxlOmluaXRpYWw7dGV4dC1pbmRlbnQ6MHB4O3RleHQtdHJhbnNmb3JtOm5vbmU7d2hpdGUtc3BhY2U6bm9ybWFsO3dvcmQtc3BhY2luZzowcHgiPm5hbWU90JjRgdGC0L7Rh9C90LjQuiDQotC10YHRgiDQotC10YHRgtC-0LLQuNGHPC9kaXY-PGRpdiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjpyZ2IoIDI1NSAsIDI1NSAsIDI1NSApO2NvbG9yOnJnYiggMzQgLCAzNCAsIDM0ICk7Zm9udC1mYW1pbHk6J2FyaWFsJyAsICdoZWx2ZXRpY2EnICwgc2Fucy1zZXJpZjtmb250LXNpemU6c21hbGw7Zm9udC1zdHlsZTpub3JtYWw7Zm9udC13ZWlnaHQ6NDAwO3RleHQtZGVjb3JhdGlvbi1zdHlsZTppbml0aWFsO3RleHQtaW5kZW50OjBweDt0ZXh0LXRyYW5zZm9ybTpub25lO3doaXRlLXNwYWNlOm5vcm1hbDt3b3JkLXNwYWNpbmc6MHB4Ij5waG9uZT0yMjIzMzIyPC9kaXY-PGRpdiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjpyZ2IoIDI1NSAsIDI1NSAsIDI1NSApO2NvbG9yOnJnYiggMzQgLCAzNCAsIDM0ICk7Zm9udC1mYW1pbHk6J2FyaWFsJyAsICdoZWx2ZXRpY2EnICwgc2Fucy1zZXJpZjtmb250LXNpemU6c21hbGw7Zm9udC1zdHlsZTpub3JtYWw7Zm9udC13ZWlnaHQ6NDAwO3RleHQtZGVjb3JhdGlvbi1zdHlsZTppbml0aWFsO3RleHQtaW5kZW50OjBweDt0ZXh0LXRyYW5zZm9ybTpub25lO3doaXRlLXNwYWNlOm5vcm1hbDt3b3JkLXNwYWNpbmc6MHB4Ij5lbWFpbD1pc3RvY2huaWstc3BiQHlhbmRleC5ydTwvZGl2PjxkaXYgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6cmdiKCAyNTUgLCAyNTUgLCAyNTUgKTtjb2xvcjpyZ2IoIDM0ICwgMzQgLCAzNCApO2ZvbnQtZmFtaWx5OidhcmlhbCcgLCAnaGVsdmV0aWNhJyAsIHNhbnMtc2VyaWY7Zm9udC1zaXplOnNtYWxsO2ZvbnQtc3R5bGU6bm9ybWFsO2ZvbnQtd2VpZ2h0OjQwMDt0ZXh0LWRlY29yYXRpb24tc3R5bGU6aW5pdGlhbDt0ZXh0LWluZGVudDowcHg7dGV4dC10cmFuc2Zvcm06bm9uZTt3aGl0ZS1zcGFjZTpub3JtYWw7d29yZC1zcGFjaW5nOjBweCI-aXNfY3VzdG9tZXI9PHN0cm9uZz5UcnVlPC9zdHJvbmc-PC9kaXY-PGRpdiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjpyZ2IoIDI1NSAsIDI1NSAsIDI1NSApO2NvbG9yOnJnYiggMzQgLCAzNCAsIDM0ICk7Zm9udC1mYW1pbHk6J2FyaWFsJyAsICdoZWx2ZXRpY2EnICwgc2Fucy1zZXJpZjtmb250LXNpemU6c21hbGw7Zm9udC1zdHlsZTpub3JtYWw7Zm9udC13ZWlnaHQ6NDAwO3RleHQtZGVjb3JhdGlvbi1zdHlsZTppbml0aWFsO3RleHQtaW5kZW50OjBweDt0ZXh0LXRyYW5zZm9ybTpub25lO3doaXRlLXNwYWNlOm5vcm1hbDt3b3JkLXNwYWNpbmc6MHB4Ij5pc19wZXJmb3JtZXI9PC9kaXY-PC9kaXY-PGRpdj7CoDwvZGl2PjxkaXY-LS3CoDxiciAvPtChINGD0LLQsNC20LXQvdC40LXQvCw8L2Rpdj48ZGl2PtCR0LXQt9C70Y7QtNC90YvQuSDQkNC70LXQutGB0LXQuTwvZGl2PjxkaXY-KDgxMikgOTIwLTQ4LTI0PC9kaXY-PGRpdj7CoDwvZGl2Pg=="

#decoded_bytes = base64.urlsafe_b64decode(str6)
#decoded_str = decoded_bytes.decode('utf-8')
#print(decoded_str)

str5 = """
email:  ohmanyukov@mail.ru , id: None, is_customer: True, is_performer: None, name: Ольга Охманюк, phone: '+79246432292'
name=\"Бобылев Евгений\"; phone=+79247401790; email=gomirka@mail.ru; is_customer=True
--
Eugeny Bobylev
"""
#persons = create_persons_from_mail_data(str5)
#for p in persons:
#    print(p)

#person2 = get_person_from_mail(str2)
#print(person2)

