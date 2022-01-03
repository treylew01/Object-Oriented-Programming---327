from datetime import datetime

class Accounts:
    def __init__(self):
        self.account_type = type
        self.number: float
        self.balance = 0
        self.transactions = []
        self.interest_rate: float

    def create_account(number):
        """creates an account based on the number that the account was created in"""
        date = str(datetime.now())
        the_date = date [0:10]
        the_month = date[5:7]

        account_type = input("Type of account? (checking/savings)\n>")
        initial_deposit = float(input("Initial deposit amount?\n>"))
        new_transaction = Transaction(the_date, initial_deposit, False)
        if account_type == "checking":
            new = CheckingAccounts(number, initial_deposit, new_transaction, the_month, the_date)
        else:
            new = SavingsAccounts(number, initial_deposit, new_transaction, the_month, the_date)
        return new

    def __str__(self):
        """defines how the account should look when printed"""
        return f"{self.account_type}#{self.number:09},\tbalance: ${self.balance:,.2f}"

    def list_transactions(self):
        """lists all the transactions"""
        return self.transactions

    def add_transaction(self, date, amount):
        """framework for the add transaction function
        which has different processes for both the checking and saving accounts"""
        old_balance = self.balance
        if(self.balance + amount < 0):
            self.balance = old_balance
        else:
            self.balance += amount
            new_transaction = Transaction(date, amount, False)
            self.transactions.append(new_transaction)

    def monthly_trigger(self):
        date = str(datetime.now())
        the_date = date [0:10]
        interest = self.balance * self.interest_rate
        self.balance += interest
        new_transaction = Transaction(the_date, interest, True)
        self.transactions.append(new_transaction)

    def account_number(self):
        """returns the account number"""
        return self.number


class CheckingAccounts(Accounts):
    def __init__(self, number, deposit, transaction, month, date):
        super()
        self.number = number
        self.balance = deposit
        self.account_type = "Checking"
        self.interest_rate = .001
        self.transactions = [transaction]

    def monthly_trigger(self):
        date = str(datetime.now())
        the_date = date [0:10]
        interest = self.balance * self.interest_rate
        self.balance += interest
        new_transaction = Transaction(the_date, interest, True)
        self.transactions.append(new_transaction)
        if self.balance <= 100:
            self.balance -= 10
            new_transaction2 = Transaction(the_date, 10, True)
            self.transactions.append(new_transaction2)


class SavingsAccounts(Accounts):
    def __init__(self, number, deposit, transaction, month, date):
        super()
        self.number = number
        self.balance = deposit
        self.account_type = "Savings"
        self.transactions = [transaction]
        self.transaction_dates_month = [month]
        self.transaction_dates = [date]
        self.interest_rate = .02

    def add_transaction(self, date, amount):
        month = date[5:7]
        amount_per_day = self.transaction_dates.count(date)
        amount_this_month = self.transaction_dates_month.count(month)
        old_balance = self.balance
        if(self.balance + amount < 0):
            self.balance = old_balance
        elif(amount_per_day >= 2):
            self.balance = old_balance
        elif(amount_this_month >= 5):
            self.balance = old_balance
        else:
            self.balance += amount
            new_transaction = Transaction(date, amount, False)
            self.transactions.append(new_transaction)
            #YYYY-MM-DD
            self.transaction_dates_month.append(month)
            self.transaction_dates.append(date)


class Transaction:
    """transaction class which mainly creates the transaction type"""
    def __init__(self, date, balance, exemption):
        self.balance = balance
        self.date = date
        self.exemeption = False

    def __str__(self):
        """helps print formatting for string"""
        return f"{self.date}, ${self.balance:,.2f}"
