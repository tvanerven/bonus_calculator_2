import datetime
from decimal import Decimal, InvalidOperation


class Bonus:

    def __init__(
            self,
            start_date: str,
            end_date: str,
            value: Decimal,
            user_id: int,
            *args,
            **kwargs
    ):
        """
        A bonus, representing a bonus to be calculated with. Expected formats:
        start_date: A string, formatted as "dd-mm-yyyy"
        end_date: A string, formatted as "dd-mm-yyyy"
        value: a Decimal number
        user_id: A integer, representing an ID in the datebase.
        """
        self.start_date = self._validate_datetime(start_date)
        self.end_date = self._validate_datetime(end_date)
        self.user = user_id
        self.value = value

    def _validate_datetime(self, date_string):
        try:
            return datetime.datetime.strptime(
                date_string, '%d-%m-%Y'
            )
        except ValueError:
            raise ValueError(
                "The date you have entered is incorrect, likely misformatted."
            )

    def _validate_value(self, value):
        try:
            return Decimal(value)
        except InvalidOperation:
            raise InvalidOperation(
                "The value could not be converted to a Decimal"
            )


    @property
    def time_delta(self):
        return self.end_date - self.start_date


class BonusCalculator:

    def __init__(
            self,
            bonus_list: list[Bonus],
            start_date: str,
            end_date: str,
            *args,
            **kwargs
    ):
        self._bonus_list = bonus_list
        self.start_date = self._validate_datetime(start_date)
        self.end_date = self._validate_datetime(end_date)
        self.result = self._calculate_bonus()

    def _validate_datetime(self, date_string):
        try:
            return datetime.datetime.strptime(
                date_string, '%d-%m-%Y'
            )
        except ValueError:
            raise ValueError(
                "The date you have entered is incorrect, likely misformatted."
            )

    def _get_bonus_list(self) -> list[Bonus]:
        """Method to 'simulate' a database call simply to return
        a list of objects.
        """
        return self._bonus_list

    def _calculate_bonus(self) -> Decimal:
        result = Decimal(0)
        bonuses = self._get_bonus_list()
        for bonus in bonuses:
            result += Decimal(self._calculate_bonus_amount(bonus))
        return self._clean_result(result)

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

    def _clean_result(self, result: float) -> Decimal:
        return round(result.quantize(Decimal('0.01')))

