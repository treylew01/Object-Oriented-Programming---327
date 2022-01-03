import sys
import pickle

from datetime import date
from bank import Bank
from account import Accounts

class Bank_CLI:
    """Display the menu and respond to choices when run."""

    def __init__(self):
        self.bank = Bank()
        self._open_account_times = 0
        self._current = None
        self._choices = {
            "open account": self._open_account,
            "summary": self._summary,
            "select account": self._select_account,
            "list transactions": self._transactions_listed,
            "add transaction": self._add_transaction,
            "<monthly triggers>": self._monthly_trigger,
            "save": self._save,
            "load": self._load,
            "quit": self._quit,
        }

    def display_menu(self):
        print(
f"""Currently selected account: {self._current}
Enter command
open account, summary, select account, list transactions, add transaction, <monthly triggers>, save, load, quit""")


    def run(self):
        """Display the menu and respond to choices."""
        while True:
            self.display_menu()
            choice = input(">")
            action = self._choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def _open_account(self):
        """Keeps track of how many accounts have been open, and opens an account based on the specification by the prompt"""
        self._open_account_times += 1
        newaccount = Accounts.create_account(self._open_account_times)
        self.bank.add_account(newaccount)
        self._summary()

    def _summary(self):
        """returns the summary"""
        self.bank.account_summary()

    def _select_account(self):
        """handles input and grabs the proper account from the Bank Class"""
        self._summary()
        account_in_list =  int(input("Enter account number\n>"))
        self._current = self.bank.account_picker(account_in_list)

    def _add_transaction(self):
        """adds a transaction to the specific account"""
        date =  input("Date? (YYYY-MM-DD)\n>")
        amount =  int(input("Amount?\n>"))
        self.bank.transactions(self._current, date, amount)

    def _transactions_listed(self):
        """lists all the transactions"""
        self.bank.transaction_list(self._current)

    def _monthly_trigger(self):
        self.bank.transaction_monthly()

    def _save(self):
        with open("bank_save.pickle", "wb") as f:
            pickle.dump(self.bank, f)

    def _load(self):
        with open("bank_save.pickle", "rb") as f:
            self.bank = pickle.load(f)

    def _quit(self):
        sys.exit(0)


if __name__ == "__main__":
    Bank_CLI().run()
