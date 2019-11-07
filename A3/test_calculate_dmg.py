from unittest import TestCase
from unittest.mock import patch

from A3 import sud


class TestCalculate_dmg(TestCase):

    @patch('random.randint', return_value=6)
    def test_calculate_dmg(self, mock_roll):
        class_list = ['barbarian', 'paladin', 'fighter', 'ranger', 'bard', 'cleric', 'druid', 'monk', 'rogue',
                      'warlock', 'wizard', 'sorcerer']

        for i in class_list:
            self.assertEqual(6, sud.calculate_dmg(True, i))

    def test_calculate_dmg_no_hit(self):
        class_list = ['barbarian', 'paladin', 'fighter', 'ranger', 'bard', 'cleric', 'druid', 'monk', 'rogue',
                      'warlock', 'wizard', 'sorcerer']

        for i in class_list:
            self.assertEqual(0, sud.calculate_dmg(False, i))
