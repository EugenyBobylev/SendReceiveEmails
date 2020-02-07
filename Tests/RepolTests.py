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

    def test_add_persons(self):
        person1 = Person()
        person1.name = "Ольга"
        person2 = Person()
        person2.name = "Олег"
        persons = [person1, person2]
        results = self.repo.add_persons(persons)

        self.assertTrue(len(results) == 2)
        self.assertEqual(1, results[0]['person'].id )