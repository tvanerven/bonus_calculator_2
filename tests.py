from unittest import TestCase
from decimal import Decimal

from calculator import Bonus, BonusCalculator


class BonusCalculatorTestCase(TestCase):

    def test_scripted_scenario(self):
        first_bonus = Bonus(
            start_date='01-01-2019',
            end_date='01-01-2020',
            value=100,
            user_id=1
        )
        second_bonus = Bonus(
            start_date='01-01-2020',
            end_date='01-01-2021',
            value=200,
            user_id=1
        )
        bonus = BonusCalculator(
            bonus_list=[first_bonus, second_bonus],
            start_date='01-07-2019',
            end_date='01-01-2021'
        )
        self.assertEqual(
            bonus.result,
            Decimal('250.00')
        )
