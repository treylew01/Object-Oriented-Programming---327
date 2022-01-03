from Transactions import Transaction
from errorrs import TransactionLimitError, TransactionOrderError, OverdrawError
from MyTime import Base, MyTime

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import functools
from sqlalchemy.types import TypeDecorator

class Account(Base):
    """This is an abstract class for accounts.  Provides default functionality for adding transactions, getting balances, and assessing interest and fees.
    Accounts should be instantiated as SavingsAccounts or CheckingAccounts
    """
    __tablename__ = "account"

    _transactions = relationship("Transaction")
    _bank_id = Column(Integer, ForeignKey("bank._id"))

    _account_number = Column(Integer, primary_key = True)
    _lastest_date = Column(MyTime(length=10))

    _interest_rate = Column(Float)

    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'account',
        'polymorphic_on':type
    }

    def __init__(self, acct_num):
        #self._transactions = []
        self._account_number = acct_num
        self._lastest_date = None

    def add_transaction(self, t, session):
        """Checks a pending transaction to see if it is allowed and adds it to the account if it is.

        Args:
            t (Transaction): incoming transaction
        """


        new_date = t.get_date()
        current_date = self._lastest_date

        balance_ok = self._check_balance(t)
        limits_ok = self._check_limits(t)

        if t.is_exempt():
            self._transactions.append(t)
            session.add(t)
        else:
            if self._lastest_date == None or current_date <= new_date:
                if self._check_balance(t):
                    pass
                else:
                    raise OverdrawError()

                if t.is_exempt() or (balance_ok and limits_ok):
                    self._transactions.append(t)
                    self._lastest_date = t.get_date()
                    session.add(t)
            else:
                raise TransactionOrderError()


    def _check_balance(self, t):
        """Checks whether an incoming transaction would overdraw the account

        Args:
            t (Transaction): pending transaction

        Returns:
            bool: false if account is overdrawn
        """


        return t.check_balance(self.get_balance())

    def _check_limits(self, t):
        return True

    def get_balance(self):
        """Gets the balance for an account by summing its transactions

        Returns:
            float: current balance
        """
        # could have a balance variable updated when transactions are added (or removed) which is faster
        # but this is more foolproof since it's always in sync with transactions
        return sum(x for x in self._transactions)

    def get_latest_date(self):
        return self._lastest_date

    def assess_interest(self, session):
        """Calculates interest for an account balance and adds it as a new transaction exempt from limits.
        """
        #print(self.get_balance() * self._interest_rate)
        t = Transaction(self.get_balance() * self._interest_rate, exempt=True)
        session.add(t)
        self.add_transaction(t, session)

    def assess_fees(self, session):
        pass

    def get_account_number(self):
        return self._account_number

    def __str__(self):
        """Formats the account number and balance of the account.
        For example, '#000000001,<tab>balance: $50.00'
        """
        return f"#{self._account_number:09},\tbalance: ${self.get_balance():,.2f}"

    def get_transactions(self):
        return self._transactions


class SavingsAccount(Account):
    """Concrete Account class with daily and monthly account limits and high interest rate.
    """
    #_interest_rate = Column(Float)
    _daily_limit = Column(Integer)
    _monthly_limit = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity':'savingsaccount',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._interest_rate = 0.02
        self._daily_limit = 2
        self._monthly_limit = 5

    def _check_limits(self, t1:Transaction) -> bool:
        """determines if the incoming trasaction is within the accounts transaction limits

        Args:
            t1 (Transaction): pending transaction to be checked

        Returns:
            bool: true if within limits and false if beyond limits
        """
        num_today = len(
            [t2 for t2 in self._transactions if not t2.is_exempt() and t2.in_same_day(t1)])
        num_this_month = len(
            [t2 for t2 in self._transactions if not t2.is_exempt() and t2.in_same_month(t1)])

        if num_today >= self._daily_limit or num_this_month >= self._monthly_limit:
            raise TransactionLimitError()

        return num_today < self._daily_limit and num_this_month < self._monthly_limit

    def __str__(self):
        """Formats the type, account number, and balance of the account.
        For example, 'Savings#000000001,<tab>balance: $50.00'
        """
        return "Savings" + super().__str__()


class CheckingAccount(Account):
    """Concrete Account class with lower interest rate and low balance fees.
    """
    #_interest_rate = Column(Float)
    _balance_threshold = Column(Integer)
    _low_balance_fee = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity':'checkingaccount',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._interest_rate = 0.001
        self._balance_threshold = 100
        self._low_balance_fee = -10

    def assess_fees(self, session):
        """Adds a low balance fee if balance is below a particular threshold. Fee amount and balance threshold are defined on the CheckingAccount.
        """
        if self.get_balance() < self._balance_threshold:
            t = Transaction(self._low_balance_fee, exempt=True)
            self.add_transaction(t, session)
            #session.add(t)

            #session.add(t)

    def __str__(self):
        """Formats the type, account number, and balance of the account.
        For example, 'Checking#000000001,<tab>balance: $50.00'
        """
        return "Checking" + super().__str__()
