from unittest import TestCase
from unittest.mock import patch

from A3.monster import choose_monster_attack


class TestChoose_monster_attack(TestCase):
    @patch('random.choice', side_effect=['kitty', 'puppy', 'otter', 'longsword', 'AK-47', 'thermonuclear device'])
    def test_choose_monster_attack(self, mock_choice):
        attacks = ['kitty', 'puppy', 'otter', 'longsword', 'AK-47', 'thermonuclear device']

        for attack in attacks:
            self.assertEqual(choose_monster_attack(attacks), attack)
