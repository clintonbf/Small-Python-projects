import io
from unittest import TestCase
from unittest.mock import patch

from A3.sud import equip_special_item


class TestEquip_special_item(TestCase):
    def test_equip_special_item_equips_special_item(self):
        p = {'doctor-note': {'existence': False, 'durability': 0}}
        equip_special_item(1, p)

        self.assertTrue(p['doctor-note']['existence'])

    def test_equip_special_item_special_item_has_full_durability(self):
        p = {'doctor-note': {'existence': False, 'durability': 0}}
        equip_special_item(1, p)

        self.assertEqual(p['doctor-note']['durability'], 3)

    def test_equip_special_item_gets_dexterity_boost(self):
        p = {'Dexterity': 10, 'doctor-note': {'existence': False, 'durability': 0}}

        equip_special_item(1, p)

        self.assertEqual(p['Dexterity'], 99)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_equip_special_item_prints_msg(self, mock_output):
        p = {'Dexterity': 10, 'doctor-note': {'existence': False, 'durability': 0}}

        equip_special_item(1, p)

        self.assertEqual(mock_output.getvalue(), "You've found a doctor's note! This will certainly come in handy.\n")
