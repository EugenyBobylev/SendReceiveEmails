import re
import unittest
import mailparser
from models import Person


class MailparserTests(unittest.TestCase):
    def test_all_truth(self):
        assert True

    def test_get_persons_from_text(self):
        data1: str = "email: ohmanyukov@mail.ru, Id: 1234, is_customer: True, is_performer: none, " \
                     "name: Ольга Охманюк, phone: '+79246432292'"
        data2: str = "name=\"Бобылев Евгений\"; phone=+79247401790; email=gomirka@mail.ru; is_customer=True"
        data3: str = "email: ohmanyukov@mail.ru, id: None, is_customer: True, is_performer: None, name: Ольга Охманюк, phone: +79246432292 -- Eugeny Bobylev"
        person1: Person = mailparser.get_person_from_text(data1)
        person2: Person = mailparser.get_person_from_text(data2)
        person3: Person = mailparser.get_person_from_text(data3)

        self.assertIsNotNone(person1)
        self.assertIsNotNone(person2)
        self.assertIsNotNone(person3)

    def test_key_value_string_parse(self):
        kv_string = " email: ohmanyukov@mail.ru "
        result = re.findall("\\s*(.*?)\\s*[:|=]\\s*(.*)", kv_string)

        self.assertTrue(2, len(result))
        self.assertEquals("email", result[0][0])
        self.assertEquals("ohmanyukov@mail.ru ", result[0][1])


if __name__ == '__main__':
    unittest.main()