from constants import BLACK, BOARD_SIZE, WHITE, ALPHABET
from board import Board
from players import Player, HumanPlayer, RandomCompPlayer, GreedyCompPlayer, MinimaxPlayer
from copy import deepcopy
import sys

import time

from pieces_checkers import CheckerFactory
from game_state_checkers import CheckersGameState

from pieces_chess import ChessFactory
from game_state_chess import ChessGameState

import tkinter as tk

class GUI_CHESS:
    def __init__(self):


        self._window = tk.Tk()
        self._window.title("My Chess Game")

        # create board, set up, and initialize game state
        b = Board(int(BOARD_SIZE), ChessFactory())
        b.set_up()
        self._game_state = ChessGameState(b, WHITE, None)

        self._board_frame = tk.Frame(self._window)
        self._board_frame.grid(row=1, column=1, columnspan=8)

        self._end_frame = tk.Frame(self._window)
        self._end_frame.grid(row=1, column=1, columnspan=3)

        self._loading_screen = tk.Frame(self._window)
        self._loading_screen.grid(row=3, column=3, columnspan=3)

        self._loading_screen2 = tk.Frame(self._window)
        self._loading_screen2.grid(row=4, column=3, columnspan=3)

        self._loading_screen3 = tk.Frame(self._window)
        self._loading_screen3.grid(row=5, column=3, columnspan=3)

        self._loading_screen4 = tk.Frame(self._window)
        self._loading_screen4.grid(row=6, column=3, columnspan=3)

        self._loading_screen5 = tk.Frame(self._window)
        self._loading_screen5.grid(row=7, column=3, columnspan=3)

        #btn = tk.Button(self._board_frame, text="O
        self.spaces = []
        self.yellow_list = []
        self.options = []

        self._option1 = None

        self.click1 = None
        self.click2 = None
        self.click3 = None
        self.click4 = None

        #self.new_board(self._game_state)
        self.loading_screen()
        self._window.mainloop()

    def loading_screen(self):
        T = tk.Text(self._loading_screen, height = 5, width = 52)
        l = tk.Label(self._loading_screen, text = "Player1")
        l.config(font =("Comic Sans", 15))
        l.grid(row=1, column=1)
        click = tk.StringVar()
        drop1 = tk.OptionMenu(self._loading_screen, click, "human", "random", "greedy", "minimax1", "minimax2", "minimax3", "minimax4")
        drop1.grid(row=2, column=1)

        T1 = tk.Text(self._loading_screen2, height = 5, width = 52)
        l1 = tk.Label(self._loading_screen2, text = "Player2")
        l1.config(font =("Comic Sans", 15))
        l1.grid(row=1, column=1)
        click2 = tk.StringVar()
        drop2 = tk.OptionMenu(self._loading_screen2, click2, "human", "random", "greedy", "minimax1", "minimax2", "minimax3", "minimax4")
        drop2.grid(row=2, column=1)

        T2 = tk.Text(self._loading_screen3, height = 5, width = 52)
        l2 = tk.Label(self._loading_screen3, text = "Graphics")
        l2.config(font =("Comic Sans", 15))
        l2.grid(row=1, column=1)
        click3 = tk.StringVar()
        drop3 = tk.OptionMenu(self._loading_screen3, click3, "No graphics")
        drop3.grid(row=2, column=1)

        T3 = tk.Text(self._loading_screen4, height = 5, width = 52)
        l3 = tk.Label(self._loading_screen4, text = "History")
        l3.config(font =("Comic Sans", 15))
        l3.grid(row=1, column=1)
        click4 = tk.StringVar()
        drop4 = tk.OptionMenu(self._loading_screen4, click4, "History Off")
        drop4.grid(row=2, column=1)

        self.click1 = click
        self.click2 = click2
        self.click3 = click3
        self.click4 = click4

        T4 = tk.Text(self._loading_screen5, height = 5, width = 52)
        l4 = tk.Label(self._loading_screen5, text = "CLICK BUTTON WHEN READY - BEST TO CLICK ALL DROP DOWNS")
        l4.config(font =("Comic Sans", 15))
        l4.grid(row=1, column=1)
        btn = tk.Button(self._loading_screen5, text="GO", font=15, command=lambda: self.create_game(), width=8,height=4,).grid(row=2, column=2, sticky="W")


    def create_game(self):
        if self.click1.get() == "human" and self.click2.get() == "human" and self.click3.get() == "No graphics" and self.click4.get() == "History Off":
            self.new_board(self._game_state)
        elif self.click1.get() != "human" and self.click2.get() != "human" and self.click3.get() == "No graphics" and self.click4.get() == "History Off":
            playerone = Player(WHITE)
            player1 = playerone.create_player(self.click1.get())
            playertwo = Player(BLACK)
            player2 = playertwo.create_player(self.click1.get())
            self.computer_moves(self._game_state, player1, player2)


    def computer_moves(self, gamestate, player1, player2):
        self._loading_screen.destroy()
        self._loading_screen2.destroy()
        self._loading_screen3.destroy()
        self._loading_screen4.destroy()
        self._loading_screen5.destroy()

        self._board_frame = tk.Frame(self._window)
        self._board_frame.grid(row=1, column=1, columnspan=8)

        while(True):
            self.new_board(gamestate)
            player1.take_turn(gamestate)
            time.sleep(3)
            player2.take_turn(gamestate)
            time.sleep(3)


    def new_board(self, gamestate):
        self._loading_screen.destroy()
        self._loading_screen2.destroy()
        self._loading_screen3.destroy()
        self._loading_screen4.destroy()
        self._loading_screen5.destroy()

        self._board_frame = tk.Frame(self._window)
        self._board_frame.grid(row=1, column=1, columnspan=8)

        board = gamestate._board
        i = 0

        for row in range(0,8):
            for col in range(1,9):
                state = 'disabled'
                space = board.get_space(f"{ALPHABET[row]}+{col}")
                piece = space.piece
                if piece:
                    if len(piece.enumerate_moves()) > 0:
                        state = 'normal'
                    if piece._side != gamestate.current_side:
                        state = 'disabled'

                new_text = str(space.draw())
                btn = tk.Button(self._board_frame, text=str(space.draw()), state = state, font=30, command=lambda space=space: self.make_move(space, gamestate), width=8,height=4,).grid(row=col, column=row, sticky="W")
                self.spaces.append(btn)
                #self.spaces.append(btn)
                i += 1

    def make_move(self, space, gamestate):
        space = space
        piece = space.piece

        if piece != None:
            if piece._side == gamestate.current_side:
                yellow_list = []
                options = piece.enumerate_moves()
                for option in options:
                    yellow_list.append(option._end)
                self.yellow_list = yellow_list
                self.options = options

        if len(self.yellow_list) != 0:
            if space in self.yellow_list:
                for option in self.options:
                    if option._end == space:
                        option.execute(gamestate)
                        self.yellow_list = []
            self.new_board

        if self._game_state.check_loss():
            if self._game_state.current_side == WHITE:
                self._board_frame.destroy()
                T = tk.Text(self._end_frame, height = 5, width = 52)

                # Create label
                l = tk.Label(self._end_frame, text = "BLACK HAS WON")
                l.config(font =("Comic Sans", 30))

                T.pack()
                l.pack()

                self._end_frame = tk.Frame(self._window)
                self._end_frame.grid(row=1, column=1, columnspan=1)
                return
            else:
                self._board_frame.destroy()

                T = tk.Text(self._end_frame, height = 5, width = 52)

                # Create label
                l = tk.Label(self._end_frame, text = "WHITE HAS WON")
                l.config(font =("Comic Sans", 30))

                T.pack()
                l.pack()

                self._end_frame = tk.Frame(self._window)
                self._end_frame.grid(row=1, column=1, columnspan=1)
                return


        if self._game_state.check_draw():
            self._board_frame.destroy()

            T = tk.Text(self._end_frame, height = 5, width = 52)

            # Create label
            l = tk.Label(self._end_frame, text = "WHITE HAS WON")
            l.config(font =("Comic Sans", 30))

            T.pack()
            l.pack()

            self._end_frame = tk.Frame(self._window)
            self._end_frame.grid(row=1, column=1, columnspan=1)
            return

        board = gamestate._board
        i = 0
        for row in range(0,8):
            for col in range(1,9):
                state = 'disabled'
                space = board.get_space(f"{ALPHABET[row]}+{col}")
                piece = space.piece
                if piece:
                    if len(piece.enumerate_moves()) > 0:
                        state = 'normal'
                    if piece._side != gamestate.current_side:
                        state = 'disabled'
                space = board.get_space(f"{ALPHABET[row]}+{col}")
                new_text = str(space.draw())
                if space in self.yellow_list:
                    btn = tk.Button(self._board_frame, text=str(space.draw()), bg = "yellow",font=30, command=lambda space=space: self.make_move(space, gamestate), width=8,height=4,).grid(row=col, column=row, sticky="W")
                else:
                    btn = tk.Button(self._board_frame, text=str(space.draw()), state = state, font=30, command=lambda space=space: self.make_move(space, gamestate), width=8,height=4,).grid(row=col, column=row, sticky="W")
                self.spaces.append(btn)
                #self.spaces.append(btn)
                i += 1





        #self.new_board(gamestate)

#        logging.basicConfig(format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %I:%M:%S', filename='bank.log', level=logging.DEBUG)

#        self._window = tk.Tk()
#        self._window.report_callback_exception = handle_exception

#        self._window.title("BANK")

#        self._bank = self._session.query(Bank).first()
#        logging.debug("Loaded from bank.db")
#        if not self._bank:
#            self._bank = Bank()
#            self._session.add(self._bank)
#            self._session.commit()

        #helps with buttons
#        self._options_frame = tk.Frame(self._window)
        #window will appear when you open a new accounts
#        self._open_account_frame = tk.Frame(self._window)
        #window will appear when you add a new transaction
#        self._add_transaction_frame = tk.Frame(self._window)
        #shows the accounts in a frame
#        self._accounts_frame = tk.Frame(self._window)
#        #shows the transactions in a frame
#        self._transaction_frame = tk.Frame(self._window)


#        self._highlight = tk.Label(text = "Selected Account: ")
#        self._highlight.grid(row=0, column = 1, columnspan=5)


#        self._open_account_frame.grid(row=2, column=1, columnspan=1, sticky="w")
#        self._transaction_frame.grid(row=3, column=1, columnspan=3, sticky="e")
#        self._add_transaction_frame.grid(row=2, column=1, columnspan=1, sticky="e")
        #self._note_frame.grid(row=1, column=2, columnspan=1)

#        tk.Button(self._options_frame, text="Add Transaction", command=self._add_transaction).grid(row=2, column=2),
#        tk.Button(self._options_frame, text="<monthly triggers>", command=self._monthly_triggers).grid(row=2, column=3),

#        self._option = tk.IntVar()

#        self._select_account = None

        #self._accounts = {}

        #self._show_accounts()
        #self._window.mainloop()
