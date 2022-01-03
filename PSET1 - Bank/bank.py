from account import Accounts

class Bank:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        """adds account, and mainly works with account class"""
        self.accounts.append(account)

    def bank_size(self):
        """returns the size of the bank, i.e how many accounts"""
        print(self.account_numbers)

    def account_summary(self):
        """returns the account summary, or the different types of accounts in the bank"""
        for account in self.accounts:
            print(str(account))

    def account_picker(self, number):
        """returns the proper account to the user from the bank"""
        return self.accounts[number - 1]

    def transactions(self, account, date, amount):
        """aids in creating the transaction, calls on account class functions"""
        if account in self.accounts:
            account.add_transaction(date, amount)
            return account

    def transaction_list(self, account):
        """keeps track of the transaction list, mainly uses the transaction list in the account class"""
        if account in self.accounts:
            list = account.list_transactions()
            for x in list:
                print(str(x))

    def transaction_monthly(self):
        """Triggers the monthly transactions"""
        for account in self.accounts:
            account.monthly_trigger()
