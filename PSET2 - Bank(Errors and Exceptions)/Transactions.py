from datetime import datetime
from errorrs import OverdrawError,  DollarError, DateError
from MyTime import Base, MyTime

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Float, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import functools
from sqlalchemy.types import TypeDecorator


class Transaction(Base):

    __tablename__ = "transaction"

    _id = Column(Integer, primary_key=True)
    _account_id = Column(Integer, ForeignKey("account._account_number"))

    _amt = Column(Float)
    _exempt = Column(Boolean)
    _date = Column(MyTime(length=10))


    def __init__(self, amt, date=None, exempt=False):
        try:
            if date is None:
                self._date = datetime.now().date()
            else:
                self._date = datetime.strptime(date, "%Y-%m-%d").date()
            self._exempt = exempt
        except ValueError:
            raise DateError()

        try:
            self._amt = float(amt)
        except ValueError:
            raise DollarError()


    def __str__(self):
        return f"{self._date}, ${self._amt:,.2f}"

    def get_date(self):
        return self._date

    def is_exempt(self):
        return self._exempt

    def in_same_day(self, other):
        return self._date == other._date

    def in_same_month(self, other):
        return self._date.month == other._date.month and self._date.year == other._date.year

    def __radd__(self, other):
        # allows us to use sum() with transactions
        return other + self._amt

    def check_balance(self, balance):
        #if self._amt < 0:
        #    raise OverdrawError()

        return self._amt >= 0 or balance > abs(self._amt)
