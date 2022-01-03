import sys
import pickle

from Bank import Bank
from Transactions import Transaction
from errorrs import OverdrawError, TransactionLimitError, DollarError, DateError, TransactionOrderError
import logging
from MyTime import Base

import sqlalchemy
from sqlalchemy.orm.session import sessionmaker


class BankCLI():
    def __init__(self):
        logging.basicConfig(format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %I:%M:%S', filename='bank.log', level=logging.DEBUG)

        self._session = Session()
        self._bank = self._session.query(Bank).first()
        logging.debug("Loaded from bank.db")
        if not self._bank:
            self._bank = Bank()
            self._session.add(self._bank)
            self._session.commit()
            logging.debug("Saved to bank.db")
        self._selected_account = None
        self._choices = {
            "open account": self._open_account,
            "summary": self._summary,
            "select account": self._select,
            "list transactions": self._list_transactions,
            "add transaction": self._add_transaction,
            "<monthly triggers>": self._monthy_triggers,
            "save": self._save,
            "load": self._load,
            "quit": self._quit,
        }


    def _display_menu(self):
        print(f"Currently selected account: {self._selected_account}")
        options = ", ".join(self._choices.keys())
        print('Enter command')
        print(options)

    def run(self):
        """Display the menu and respond to choices."""

        try:
            while True:
                self._display_menu()
                choice = input(">")
                action = self._choices.get(choice)
                if action:
                    action()
                else:
                    print("{0} is not a valid choice".format(choice))
        except Exception as err:
            typeof = err.__class__.__name__
            message =  getattr(err, 'message', err)
            logging.error(f"{typeof}: {message}")
            print("Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
            sys.exit(0)



    def _summary(self):
        for x in self._bank.show_accounts():
            print(x)


    def _load(self):
        with open("bank.pickle", "rb") as f:
            self._bank = pickle.load(f)
            logging.debug("Loaded from bank.pickle")

    def _save(self):

        with open("bank.pickle", "wb") as f:
            pickle.dump(self._bank, f)
            logging.debug("Saved to bank.pickle")


    def _quit(self):
        sys.exit(0)

    def _add_transaction(self):
        try:
            date = input("Date? (YYYY-MM-DD)\n>")
            amount = input("Amount?\n>")

            t = Transaction(amount, date)

            self._selected_account.add_transaction(t, self._session)

        except DateError:
            print("Please try again with a valid date in the format YYYY-MM-DD.")
        except DollarError:
            print("Please try again with a valid dollar amount.")
        except AttributeError:
            print("That command requires that you first select an account.")
        except OverdrawError:
            print("This transaction could not be completed due to an insufficient account balance.")
        except TransactionLimitError:
            print("This transaction could not be completed because the account has reached a transaction limit.")
        except TransactionOrderError:
            print(f"New transactions must be from {self._selected_account.get_latest_date()} onward.")

        logging.debug(f"Created transaction: {self._selected_account.get_account_number()}, {t._amt:,.2f}")
        self._session.commit()
        logging.debug("Saved to bank.db")

        #self._selected_account.add_transaction(t)

    def _open_account(self):
        try:
            type = input("Type of account? (checking/savings)\n>")
            initial_deposit = input("Initial deposit amount?\n>")

            t = Transaction(initial_deposit)

            a = self._bank.add_account(type, self._session)
            a.add_transaction(t, self._session)

            self._summary()
        except DollarError:
            print("Please try again with a valid dollar amount.")

        newbanknum = self._bank._generate_account_number() - 1
        logging.debug(f"Created account: {newbanknum}")
        logging.debug(f'Created transaction: {newbanknum}, {t._amt:,.2f}')
        self._session.commit()
        logging.debug("Saved to bank.db")


    def _select(self):
        self._summary()
        num = int(input("Enter account number\n>"))
        self._selected_account = self._bank.get_account(num)

    def _monthy_triggers(self):
        self._bank.assess_interest(self._session)
        self._bank.assess_fees(self._session)

        logging.debug("Triggered fees and interest")

        self._session.commit()
        logging.debug("Saved to bank.db")

    def _list_transactions(self):
        for x in self._selected_account.get_transactions():
            print(x)


if __name__ == "__main__":

     engine = sqlalchemy.create_engine(f"sqlite:///bank.db")
     Base.metadata.create_all(engine)

     Session = sessionmaker()
     Session.configure(bind=engine)

     BankCLI().run()
