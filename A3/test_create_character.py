from unittest import TestCase

from A3 import character


class TestCreate_character(TestCase):
    def test_create_character_attributes(self):
        c = character.create_character()

        expected_attr = {'Name': 'Anonymous', 'Dexterity': 0, 'Class': 'student', 'HP': {'Current': 10, 'Max': 10}}

        for k in c:
            self.assertEqual(c[k], expected_attr[k])