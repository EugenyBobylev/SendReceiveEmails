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
        result: Dict[bool, Person] = self.repo.add_person(person)
        person = result['person']
        person.email = 'olga@mail.ru'
        person.phone = '+79247401790'

        result2 = self.repo.update_person(person)
        person2 = result['person']
        self.assertTrue(result2['ok'])
        self.assertEqual('olga@mail.ru', person2.email)
        self.assertEqual('+79247401790', person2.phone)

    def test_get_non_exist_person(self):
        person = self.repo.get_person(0)
        self.assertIsNone(person)

    def test_get_person(self):
        person = Person()
        person.name = "Ольга"
        self.repo.add_person(person)

        person1 = self.repo.get_person(1)
        self.assertEqual(1, person1.id)