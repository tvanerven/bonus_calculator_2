import datetime
from decimal import Decimal, InvalidOperation
from typing import Union


def validate_datetime(date_string):
        try:
            return datetime.datetime.strptime(
                date_string, '%d-%m-%Y'
            )
        except ValueError:
            raise ValueError(
                "The date you have entered is incorrect, likely misformatted."
            )


def validate_value(value):
    try:
        return Decimal(value)
    except InvalidOperation:
        raise InvalidOperation(
            "The value could not be converted to a Decimal"
        )


class Bonus:

    def __init__(
            self,
            identifier: int,
            start_date: str,
            end_date: str,
            value: Decimal,
            user_id: int,
            is_percentage: bool = False,
            *args,
            **kwargs
    ):
        """
        A bonus, representing a bonus to be calculated with. Expected formats:
        id: An id to provide a unique reference per bonus.
        start_date: A string, formatted as "dd-mm-yyyy"
        end_date: A string, formatted as "dd-mm-yyyy"
        value: a Decimal number
        user_id: A integer, representing an ID in the datebase.
        is_percentage: A boolean, to show if the value is a percentage or
        strict value
        """
        self.identifier = identifier
        self.start_date = validate_datetime(start_date)
        self.end_date = validate_datetime(end_date)
        self.user = user_id
        self.value = validate_value(value)
        self.is_percentage = is_percentage


class Salary:

    def __init__(
            self,
            identifier: int,
            user_id: int,
            value: Union[Decimal, int],
            *args,
            **kwargs
    ):
        """A table representing a salary.
        identifier: An identifier in a table
        user_id: A foreignkey relating to user
        value: A value assumed to be the monthly salary
        """
        self.identifier = identifier
        self.user_id = user_id
        self.value = validate_value(value)


class BonusCalculator:

    def __init__(
            self,
            bonus_list: list[Bonus],
            start_date: str,
            end_date: str,
            salaries: list[Salary] = [],
            *args,
            **kwargs
    ):
        self._bonus_list = bonus_list
        self._salaries = salaries
        self.start_date = validate_datetime(start_date)
        self.end_date = validate_datetime(end_date)
        self.value_bonus = self._calculate_value_bonuses()
        self.percentage_bonus = self._calculate_percentage_bonus()
        self.total_bonus = self._calculate_total_bonus()

    def _get_bonus_list(self) -> list[Bonus]:
        """Method to 'simulate' a database call simply to return
        a list of objects.
        """
        return self._bonus_list

    def _get_salaries_for_user(self, bonus: Bonus) -> Decimal:
        """Another method to 'simulate' a database call."""
        for salary in self._salaries:
            if salary.user_id == bonus.user:
                return salary

    def _calculate_percentage_bonus(self) -> Decimal:
        result = {}
        bonuses = self._get_bonus_list()
        percentage_bonuses = [
            percentage_bonus for percentage_bonus in bonuses
            if percentage_bonus.is_percentage
        ]
        for bonus in percentage_bonuses:
            salary_for_user = self._get_salaries_for_user(bonus)
            percentage = Decimal(self._calculate_bonus_amount(bonus))
            result[bonus.identifier] = \
                (percentage / 100 ) * salary_for_user.value
        return self._clean_result(result)

    def _calculate_value_bonuses(self) -> Decimal:
        result = Decimal(0)
        bonuses = self._get_bonus_list()
        value_bonuses = [
            value_bonus for value_bonus in bonuses
            if value_bonus.is_percentage is False
        ]
        for bonus in value_bonuses:
            result += Decimal(self._calculate_bonus_amount(bonus))
        return self._clean_result(result)

    def _calculate_total_bonus(self) -> Decimal:
        bonus_total = self.value_bonus
        for key, value in self.percentage_bonus.items():
            bonus_total += value
        return bonus_total

    def _calculate_bonus_amount(self, bonus: Bonus) -> Decimal:
        if (
            self.start_date <= bonus.start_date
        ) and (
            self.end_date >= bonus.start_date
        ):
            # Case 1. Bonus fully applies since the dates are within the timeframe.
            return bonus.value
        elif (
            self.start_date >= bonus.start_date
        ) and (
            self.end_date >= bonus.end_date
        ):
            # Case 2. The start date is later than the bonus start date, but
            # the bonus ends earlier than the end date. Partial amount.
            return self._calculate_partial_finished_bonus(bonus)
        elif self.end_date <= bonus.start_date:
            # Case 3. The start date of the bonus is not in range.
            # It mustn't be applied.
            return Decimal('0')
        elif (
                self.start_date >= bonus.start_date
        ) and (
            self.end_date <= bonus.end_date
        ):
            # Case 4: The start date is later than the bonus start date,
            # but the bonus hasn't ended yet at the end date. Partial amount.
            return self._calculate_partial_unfinished_bonus(bonus)

    def _calculate_partial_finished_bonus(self, bonus: Bonus) -> Decimal:
        start_delta = self.start_date - bonus.start_date
        complete_bonus_time = bonus.end_date - bonus.start_date
        partial_bonus_time = complete_bonus_time - start_delta
        value_per_day = bonus.value / complete_bonus_time.days
        partial_bonus = partial_bonus_time.days * value_per_day
        return partial_bonus

    def _calculate_partial_unfinished_bonus(self, bonus: Bonus) -> Decimal:
        end_delta = self.end_date - bonus.end_date
        complete_bonus_time = bonus.end_date - bonus.start_date
        partial_bonus_time = complete_bonus_time - end_delta
        value_per_day = bonus.value / complete_bonus_time.days
        partial_bonus = partial_bonus_time.days * value_per_day
        return partial_bonus

    def _clean_result(self, result: Union[Decimal, dict]) -> Decimal:
        if isinstance(result, Decimal):
            return round(result.quantize(Decimal('0.01')))
        if isinstance(result, dict):
            cleaned_result = {}
            for key, value in result.items():
                cleaned_result[key] = round(value.quantize(Decimal('0.01')))
            return cleaned_result
