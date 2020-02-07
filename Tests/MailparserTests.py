import re
import unittest
import mailparser
from models import Person


class MailparserTests(unittest.TestCase):
    def test_get_persons_from_text(self):
        data1: str = "email: ohmanyukov@mail.ru, Id: 1234, is_customer: True, is_performer: none, " \
                     "name: Ольга Охманюк, phone: '+79246432292'"
        data2: str = "name=\"Бобылев Евгений\"; phone=+79247401790; email=gomirka@mail.ru; is_customer=True"
        data3: str = "email: ohmanyukov@mail.ru, id: None, is_customer: True, is_performer: None, name: Ольга Охманюк, phone: +79246432292 -- Eugeny Bobylev"
        data4: str = "id=1; name=Бобылев; email=; phone=; is_customer=False"
        person1: Person = mailparser.get_person_from_text(data1)
        person2: Person = mailparser.get_person_from_text(data2)
        person3: Person = mailparser.get_person_from_text(data3)
        person4: Person = mailparser.get_person_from_text(data4)

        self.assertIsNotNone(person1)
        self.assertIsNotNone(person2)
        self.assertIsNotNone(person3)
        self.assertIsNotNone(person4)

    def test_key_value_string_parse(self):
        kv_string = " email: ohmanyukov@mail.ru "
        result = re.findall("\\s*(.*?)\\s*[:|=]\\s*(.*)", kv_string)

        self.assertTrue(2, len(result))
        self.assertEquals("email", result[0][0])
        self.assertEquals("ohmanyukov@mail.ru ", result[0][1])

    def test_create_persons_from_mail_data(self):
        str = """
email:  ohmanyukov@mail.ru , id: None, is_customer: True, is_performer: None, name: Ольга Охманюк, phone: '+79246432292'
name=\"Бобылев Евгений\"; phone=+79247401790; email=gomirka@mail.ru; is_customer=True
--
Eugeny Bobylev
"""
        persons = mailparser.create_persons_from_mail_data(str)
        self.assertEquals(2, len(persons))

    def test_2_create_persons_from_mail_data(self):
        str = "id=1; phone=+79247401790"
        persons = mailparser.create_persons_from_mail_data(str)
        self.assertEquals(1, len(persons))

if __name__ == '__main__':
    unittest.main()
