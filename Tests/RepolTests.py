import unittest
from typing import Dict
from repo import Repo, Person


class RepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Repo()

    def test_add_person(self):
        person = Person()
        person.name = "Ольга"
        result: Dict[bool, Person] = self.repo.add_person(person)

        self.assertTrue(result['ok'])
        self.assertEqual("", person.email)
        self.assertEqual("", person.phone)

    def test_add_persons(self):
        person1 = Person()
        person1.name = "Ольга"
        person2 = Person()
        person2.name = "Олег"
        persons = [person1, person2]
        results = self.repo.add_persons(persons)

        self.assertTrue(len(results) == 2)
        self.assertEqual(1, results[0]['person'].id )
        self.assertEqual(2, results[1]['person'].id )

    def test_update_person(self):
        person = Person()
        person.name = "Ольга"
        result_add: Dict[bool, Person] = self.repo.add_person(person)
        self.assertTrue(result_add['ok'])

        person_data = {'id': person.id, 'email': 'xyz@contoso.com', 'phone': '+74262240149'}

        result2 = self.repo.update_person(person_data)
        person2 = self.repo.get_person(person.id)
        self.assertTrue(result2['ok'])
        self.assertEqual('xyz@contoso.com', person2.email)
        self.assertEqual('+74262240149', person2.phone)

    def test_get_non_exist_person(self):
        person = self.repo.get_person(0)
        self.assertIsNone(person)

    def test_get_person(self):
        person = Person()
        person.name = "Ольга"
        self.repo.add_person(person)

        person1 = self.repo.get_person(1)
        self.assertEqual(1, person1.id)

    def test_validate_add_person(self):
        invalid_person1 = Person()
        invalid_person1.id = 11
        is_valid1: bool = Repo.validate_add_person(invalid_person1)

        invalid_person2 = Person()
        invalid_person2.email = "contoso@mail.ru"
        is_valid2: bool = Repo.validate_add_person(invalid_person2)

        valid_person = Person()
        valid_person.name = 'Eugeny'
        is_valid3: bool = Repo.validate_add_person(valid_person)

        self.assertFalse(is_valid1)
        self.assertFalse(is_valid2)
        self.assertTrue(is_valid3)

    def test_validate_update_person(self):
        invalid_data = {'name': 'Eugeny'}
        is_valid1 = Repo.validate_update_person(invalid_data)

        valid_data = {'id': 123}
        is_valid2 = Repo.validate_update_person(valid_data)

        self.assertFalse(is_valid1)
        self.assertTrue(is_valid2)