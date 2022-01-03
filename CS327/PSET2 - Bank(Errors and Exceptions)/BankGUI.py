import tkinter as tk
from tkinter import messagebox
from tkinter import *
#from PIL import ImageTK, Image
#message.showerror()
import sys
import pickle

from Bank import Bank
from Transactions import Transaction
from errorrs import OverdrawError, TransactionLimitError, DollarError, DateError, TransactionOrderError
import logging
from MyTime import Base

import sqlalchemy
from sqlalchemy.orm.session import sessionmaker

def handle_exception(exception, value, traceback):
    tk.messagebox.error("ERROR", "Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
    logging.error(f"{exception.__name__}: {repr(value)}")
    sys.exit(1)

class Menu:
    """Display a menu and respond to choices when run."""

    def __init__(self):

        logging.basicConfig(format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %I:%M:%S', filename='bank.log', level=logging.DEBUG)

        self._window = tk.Tk()
        self._window.report_callback_exception = handle_exception

        self._window.title("BANK")

        self._session = Session()
        self._bank = self._session.query(Bank).first()
        logging.debug("Loaded from bank.db")
        if not self._bank:
            self._bank = Bank()
            self._session.add(self._bank)
            self._session.commit()

        #helps with buttons
        self._options_frame = tk.Frame(self._window)
        #window will appear when you open a new accounts
        self._open_account_frame = tk.Frame(self._window)
        #window will appear when you add a new transaction
        self._add_transaction_frame = tk.Frame(self._window)
        #shows the accounts in a frame
        self._accounts_frame = tk.Frame(self._window)
        #shows the transactions in a frame
        self._transaction_frame = tk.Frame(self._window)


        self._highlight = tk.Label(text = "Selected Account: ")
        self._highlight.grid(row=0, column = 1, columnspan=5)


        self._options_frame.grid(row=1, column=1, columnspan=2)
        self._accounts_frame.grid(row=4, column=1, columnspan=1, sticky="w")
        self._open_account_frame.grid(row=2, column=1, columnspan=1, sticky="w")
        self._transaction_frame.grid(row=3, column=1, columnspan=3, sticky="e")
        self._add_transaction_frame.grid(row=2, column=1, columnspan=1, sticky="e")
        #self._note_frame.grid(row=1, column=2, columnspan=1)

        tk.Button(self._options_frame, text="Open Account", command=self._open_account).grid(row=2, column=1),
        tk.Button(self._options_frame, text="Add Transaction", command=self._add_transaction).grid(row=2, column=2),
        tk.Button(self._options_frame, text="<monthly triggers>", command=self._monthly_triggers).grid(row=2, column=3),

        self._option = tk.IntVar()

        self._select_account = None

        self._accounts = {}

        self._show_accounts()
        self._window.mainloop()


    #adding to a specifc account
    def _add_transaction(self):
        self._open_account_frame.destroy()
        self._add_transaction_frame.destroy()

        self._add_transaction_frame = tk.Frame(self._window)
        self._add_transaction_frame.grid(row=2, column=1, columnspan=1, sticky="e")

        def add():
            try:
                date1 = e1.get()
                amount = g1.get()

                t = Transaction(amount, date=date1)

                self._select_account.add_transaction(t, self._session)
            except DateError:
                tk.messagebox.showerror("DateError", "Please try again with a valid date in the format YYYY-MM-DD.")
            except DollarError:
                tk.messagebox.showerror("DollarError", "Please try again with a valid dollar amount.")
            except AttributeError:
                tk.messagebox.showerror("AttributeError", "That command requires that you first select an account.")
            except OverdrawError:
                tk.messagebox.showerror("OverdrawError", "This transaction could not be completed due to an insufficient account balance.")
            except TransactionLimitError:
                tk.messagebox.showerror("TransactionLimitError", "This transaction could not be completed because the account has reached a transaction limit.")
            except TransactionOrderError:
                tk.messagebox.showerror("TransactionOrderError", f"New transactions must be from {self._select_account.get_latest_date()} onward.")

            self._session.commit()

            self._show_accounts()
            self._add_to_highlight()
            self._show_transactions()

            e1.destroy()
            l1.destroy()
            f1.destroy()
            g1.destroy()
            b.destroy()

            logging.debug(f"Created transaction: {self._select_account.get_account_number()}, {amount}")
            self._session.commit()
            logging.debug("Saved to bank.pickle")

            self._add_transaction_frame.destroy()

        l1 = tk.Label(self._add_transaction_frame, text="Date:")
        l1.grid(row=3, column=0)
        e1 = tk.Entry(self._add_transaction_frame)
        e1.grid(row=3, column=1)

        f1 = tk.Label(self._add_transaction_frame, text="Amount:")
        f1.grid(row=5, column=0)
        g1 = tk.Entry(self._add_transaction_frame)
        g1.grid(row=5, column=1)

        b = tk.Button(self._add_transaction_frame, text="Enter", command=add)
        b.grid(row=7, column=1)

    #opens an account
    def _open_account(self):
        self._add_transaction_frame.destroy()
        self._open_account_frame.destroy()

        self._open_account_frame = tk.Frame(self._window)
        self._open_account_frame.grid(row=2, column=1, columnspan=1, sticky="w")

        def add():
            try:
                amount = e1.get()
                t = Transaction(e1.get())
                a = self._bank.add_account(click.get(), self._session)
                a.add_transaction(t, self._session)
            except DollarError:
                tk.messagebox.showerror("DollarError", "Please try again with a valid dollar amount.")
            except AttributeError:
                tk.messagebox.showerror("AttributeError", "That command requires that you first select an account.")

            e1.destroy()
            b.destroy()
            l1.destroy()
            drop.destroy()
            self._open_account_frame.destroy()

            newbanknum = self._bank._generate_account_number() - 1
            logging.debug(f"Created account: {newbanknum}")
            logging.debug(f"Created transaction: {newbanknum}, {amount}")
            self._session.commit()
            logging.debug("Saved to bank.db")

            self._show_accounts()

        l1 = tk.Label(self._open_account_frame, text="Initial Deposit:")
        l1.grid(row=0, column=1)
        e1 = tk.Entry(self._open_account_frame)
        e1.grid(row=1, column=1)

        b = tk.Button(self._open_account_frame, text="Enter", command=add)
        b.grid(row=1, column=2)

        click = tk.StringVar()
        drop = tk.OptionMenu(self._open_account_frame, click, "checking", "savings")
        drop.grid(row=3, column=1)



    #shows the list of accounts with radiobuttons
    def _show_accounts(self, accounts=None):
        self._accounts_frame.destroy()

        self._accounts_frame = tk.Frame(self._window)
        self._accounts_frame.grid(row=3, column=1, columnspan=1, sticky="ne")

        accounts = self._bank.show_accounts()
        for x in accounts:
            if x._account_number not in self._accounts:
                tk.Radiobutton(self._accounts_frame, text=x, value=x._account_number, var=self._option, command = self._selected_account).grid(column=1, sticky="w")



    #helps when switching between accounts using Radiobutton
    def _selected_account(self):
        self._select_account = self._bank.get_account(self._option.get())

        self._add_to_highlight()
        self._show_transactions()

    #what is shown at the top of the GUI
    def _add_to_highlight(self):
        self._highlight.config(text = f'Selected Account: {self._select_account}')

    #show transactions is gonna do the frame on the right
    def _show_transactions(self):
        self._transaction_frame.destroy()

        self._transaction_frame = tk.Frame(self._window, borderwidth=5, relief="sunk")
        self._transaction_frame.grid(row=3, column=2, columnspan=1, sticky="nw")

        for x in self._select_account.get_transactions():
            if x._amt >= 0:
                Label(self._transaction_frame, fg="green", text = f"{x} \n").pack()
            else:
                Label(self._transaction_frame, fg="red", text = f"{x} \n").pack()


    def _monthly_triggers(self):
        self._bank.assess_interest(self._session)
        self._bank.assess_fees(self._session)

        self._show_accounts()
        self._add_to_highlight()
        self._show_transactions()

        logging.debug("Triggered fees and interest")
        self._session.commit()
        logging.debug("Saved to bank.db")




if __name__ == "__main__":
    engine = sqlalchemy.create_engine(f"sqlite:///bank.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    Menu()
