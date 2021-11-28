from unittest import TestCase
from decimal import Decimal, InvalidOperation

from calculator import (
    Bonus,
    BonusCalculator,
    Salary,
    validate_datetime,
    validate_value
)


class BonusCalculatorTestCase(TestCase):

    def test_scripted_scenario(self):
        first_bonus = Bonus(
            identifier=1,
            start_date='01-01-2019',
            end_date='01-01-2020',
            value=100,
            user_id=1
        )
        second_bonus = Bonus(
            identifier=2,
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
        self.assertEqual(bonus.value_bonus, Decimal('250.00'))
        self.assertEqual(bonus.total_bonus, Decimal('250.00'))

    def test_percentage_scenario(self):
        first_bonus = Bonus(
            identifier=1,
            start_date='01-01-2019',
            end_date='01-01-2020',
            value=12,
            user_id=1,
            is_percentage=True
        )
        second_bonus = Bonus(
            identifier=2,
            start_date='01-01-2020',
            end_date='01-01-2021',
            value=200,
            user_id=1,
        )
        salary = Salary(
            identifier=1,
            start_date='01-01-2019',
            end_date='01-01-2021',
            value=Decimal('1000'),
            user_id=1
        )
        invalid_salary = Salary(
            identifier=2,
            start_date='01-01-2019',
            end_date='01-01-2021',
            value=Decimal('1000'),
            user_id=2
        )
        bonus = BonusCalculator(
            bonus_list=[first_bonus, second_bonus],
            start_date='01-07-2019',
            end_date='01-01-2021',
            salaries=[salary, invalid_salary]
        )
        self.assertEqual(bonus.value_bonus, 200)
        self.assertEqual(bonus.percentage_bonus, {1: Decimal('60')})
        self.assertEqual(bonus.total_bonus, Decimal('260.00'))

    def test_exceptions(self):
        with self.assertRaises(ValueError):
            validate_datetime('01/01/2019')
            validate_datetime('50-45-1')
            validate_datetime(-1)
            validate_datetime(20)
        with self.assertRaises(InvalidOperation):
            validate_value('something')
            validate_value(6.4)
            validate_value(Bonus())
