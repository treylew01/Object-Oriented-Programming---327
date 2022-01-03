from game_state import GameState
from moves_chess import ChessMoveSet
from constants import BLACK, WHITE


class ChessGameState(GameState):
    def all_possible_moves(self, side=None):
        if not side:
            side = self._current_side
        pieces = self._board.pieces_iterator(side)
        # uses CheckersMoveSet to enforce restriction on basic moves when at least once piece has a jump
        options = ChessMoveSet()
        for piece in pieces:
            options.extend(piece.enumerate_moves())
        return options

    def check_loss(self, side=None):
        if not side:
            side = self._current_side
        # no more pieces
        flag = 0
        for piece in self._board.pieces_iterator(side):
            if side == WHITE:
                if piece.type == "ki":
                    flag = 1
            if side == BLACK:
                if piece.type ==  "ki":
                    flag = 1
        if flag == 1:
            return False
        else:
            return True

    def check_loss_side(self, side=None):
        if not side:
            side = self._current_side
        # no more pieces
        flag = 0
        for piece in self._board.pieces_iterator(side):
            if side == WHITE:
                if piece.type == "ki":
                    flag = 1
            if side == BLACK:
                if piece.type ==  "ki":
                    flag = 1
        if flag == 1:
            return None
        else:
            return True
