from Accounts import SavingsAccount, CheckingAccount
from MyTime import Base

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import functools
from sqlalchemy.types import TypeDecorator

SAVINGS = "savings"
CHECKING = "checking"

class Bank(Base):

    __tablename__ = "bank"
    _id = Column(Integer, primary_key=True)
     # backref is unnecessary, but useful for the example
    _accounts = relationship("Account")

    #def __init__(self):
    #    self._accounts = []

    def add_account(self, type, session):
        """Creates a new Account object and adds it to this bank object. The Account will be a SavingsAccount or CheckingAccount, depending on the type given.

        Args:
            type (string): "Savings" or "Checking" to indicate the type of account to create

        Returns:
            Account: the account object that was created, or None if the type did not match
        """
        acct_num = self._generate_account_number()
        if type == SAVINGS:
            a = SavingsAccount(acct_num)
        elif type == CHECKING:
            a = CheckingAccount(acct_num)
        else:
            return None
        self._accounts.append(a)
        session.add(a)
        return a

    def assess_interest(self, session):
        for acct in self._accounts:
            acct.assess_interest(session)
            #session.add(acct)

    def assess_fees(self, session):
        for acct in self._accounts:
            acct.assess_fees(session)
            #session.add(acct)

    def _generate_account_number(self):
        return len(self._accounts) + 1

    def show_accounts(self):
        return self._accounts

    def get_account(self, account_num):
        """Fetches an account by its account number.

        Args:
            account_num (int): account number to seach for

        Returns:
            Account: matching account or None if not found
        """
        for x in self._accounts:
            # could be faster using dictionary
            if x._account_number == account_num:
                return x
        return None
