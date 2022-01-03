from piece import Piece
from piece_factory import PieceFactory
from constants import BLACK, WHITE

from moves_chess import ChessMove, ChessMoveSet

class ChessFactory(PieceFactory):
    "Concrete piece factory for setting up a checkers game"

    def create_piece(self, board, space):
        x = space.row
        y = space.col
        if x == 1:
            return Pawn(BLACK, board, space)
        if board.size - x == 2:
            return Pawn(WHITE, board, space)
        if x == 0 and (y == 0 or y == 7):
            return Rook(BLACK, board, space)
        if board.size - x == 1 and (y == 0 or y == 7):
            return Rook(WHITE, board, space)
        if x == 0 and (y == 1 or y == 6):
            return Knight(BLACK, board, space)
        if board.size - x == 1 and (y == 1 or y == 6):
            return Knight(WHITE, board, space)
        if x == 0 and (y == 2 or y == 5):
            return Bishop(BLACK, board, space)
        if board.size - x == 1 and (y == 2 or y == 5):
            return Bishop(WHITE, board, space)
        if x == 0 and (y == 3):
            return Queen(BLACK, board, space)
        if board.size - x == 1 and (y == 3):
            return Queen(WHITE, board, space)
        if x == 0 and (y == 4):
            return ChessKing(BLACK, board, space)
        if board.size - x == 1 and (y == 4):
            return ChessKing(WHITE, board, space)
        return None


class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♙"
            self._directions = ["ne", "n", "nw"]
        if self._side == BLACK:
            self._symbol = u"♟︎"
            self._directions = ["se", "s", "sw"]
        self.type = "pa"
        self.value = 1

    def enumerate_moves(self):
        moves = ChessMoveSet()
        for direction in self._directions:
            one_step = self._board.get_dir(self._current_space, direction)
            if direction == "n" or direction == "s":
                if one_step and one_step.is_free():
                    m = ChessMove(self._current_space, one_step)
                    moves.append(m)
                    if ((self._side == WHITE and one_step.row == 0) or
                            (self._side == BLACK and one_step.row == self._board.size - 1)):
                            m.add_promotion()
                    if (self._side == BLACK and self._current_space.row == 1) or (self._side == WHITE and self._current_space.row == self._board.size - 2):
                        the_move_after = self._board.get_dir(one_step, direction)
                        if the_move_after and the_move_after.is_free():
                            another_move = ChessMove(self._current_space, the_move_after)
                            moves.append(another_move)

            else:
                if one_step and not one_step.is_free():
                    if one_step._piece._side != self._side:
                        m = ChessMove(self._current_space, one_step, [one_step])
                        moves.append(m)
                        if ((self._side == WHITE and one_step.row == 0) or
                                (self._side == BLACK and one_step.row == self._board.size - 1)):
                                m.add_promotion()
        return moves

    def promote(self):
        return Queen(self._side, self._board, self._current_space)

class Bishop(Pawn):
    def __init__(self, team, space, board):
        super().__init__(team, space, board)
        if self._side == WHITE:
            self._symbol = u"♗"
            self._directions = ["ne", "nw", "se", "sw"]
        if self._side == BLACK:
            self._symbol = u"♝"
            self._directions = ["ne", "nw", "se", "sw"]
        self.type = "bi"
        self.value = 3

    def one_direction_movement(self, current, direction, moves):
        one_step = self._board.get_dir(current, direction)
        if one_step != None and one_step.is_free():
            final_move = ChessMove(self._current_space, one_step)
            moves.append(final_move)
            self.one_direction_movement(one_step, direction, moves)
        elif one_step != None and not one_step.is_free():
            if one_step._piece._side != self._side:
                final_move = ChessMove(self._current_space, one_step, [one_step])
                moves.append(final_move)

    def enumerate_moves(self):
        moves = ChessMoveSet()
        for direction in self._directions:
            self.one_direction_movement(self._current_space, direction, moves)
        return moves

class Rook(Bishop):
    def __init__(self, team, space, board):
        super().__init__(team, space, board)
        if self._side == WHITE:
            self._symbol = u"♖"
            self._directions = ["n", "e", "s", "w"]
        if self._side == BLACK:
            self._symbol = u"♜"
            self._directions = ["n", "e", "s", "w"]
        self.type = "ro"
        self.value = 5


class Knight(Pawn):
    def __init__(self, team, space, board):
        super().__init__(team, space, board)
        if self._side == WHITE:
            self._symbol =  u"♘"
            self._directions = ["n", "e", "s", "w"]
        if self._side == BLACK:
            self._symbol = u"♞"
            self._directions = ["n", "e", "s", "w"]
        self.type = "kn"
        self.value = 3


    def northern_moves(self, northern, space, moves):
        new_directions = ["ne", "nw"]
        if northern == "n":
            if space:
                for direction in new_directions:
                    one_step = self._board.get_dir(space, direction)
                    if one_step and one_step.is_free():
                        final_move = ChessMove(self._current_space, one_step)
                        moves.append(final_move)
                    elif one_step and not one_step.is_free():
                        if one_step._piece._side != self._side:
                            final_move = ChessMove(self._current_space, one_step, [one_step])
                            moves.append(final_move)

    def eastern_moves(self, eastern, space, moves):
        new_directions = ["ne", "se"]
        if eastern == "e":
            if space:
                for direction in new_directions:
                    one_step = self._board.get_dir(space, direction)
                    if one_step and one_step.is_free():
                        final_move = ChessMove(self._current_space, one_step)
                        moves.append(final_move)
                    elif one_step and not one_step.is_free():
                        if one_step._piece._side != self._side:
                            final_move = ChessMove(self._current_space, one_step, [one_step])
                            moves.append(final_move)

    def southern_moves(self, southern, space, moves):
        new_directions = ["se", "sw"]
        if southern == "s":
            if space:
                for direction in new_directions:
                    one_step = self._board.get_dir(space, direction)
                    if one_step and one_step.is_free():
                        final_move = ChessMove(self._current_space, one_step)
                        moves.append(final_move)
                    elif one_step and not one_step.is_free():
                        if one_step._piece._side != self._side:
                            final_move = ChessMove(self._current_space, one_step, [one_step])
                            moves.append(final_move)

    def western_moves(self, western, space, moves):
        new_directions = ["nw", "sw"]
        if western == "w":
            if space:
                for direction in new_directions:
                    one_step = self._board.get_dir(space, direction)
                    if one_step and one_step.is_free():
                        final_move = ChessMove(self._current_space, one_step)
                        moves.append(final_move)
                    elif one_step and not one_step.is_free():
                        if one_step._piece._side != self._side:
                            final_move = ChessMove(self._current_space, one_step, [one_step])
                            moves.append(final_move)

    def enumerate_moves(self):
        moves = ChessMoveSet()
        for direction in self._directions:
            the_step = self._board.get_dir(self._current_space, direction)
            if direction == "n":
                self.northern_moves(direction, the_step, moves)
            if direction == "e":
                self.eastern_moves(direction, the_step, moves)
            if direction == "s":
                self.southern_moves(direction, the_step, moves)
            if direction == "w":
                self.western_moves(direction, the_step, moves)
        return moves

class Queen(Bishop):
    def __init__(self, team, space, board):
        super().__init__(team, space, board)
        if self._side == WHITE:
            self._symbol =  u"♕"
            self._directions = ["nw", "n", "ne", "e", "se", "s", "sw", "w"]
        if self._side == BLACK:
            self._symbol =  u"♛"
            self._directions = ["nw", "n", "ne", "e", "se", "s", "sw", "w"]
        self.type = "qu"
        self.value = 9


class ChessKing(Pawn):
    def __init__(self, team, space, board):
        super().__init__(team, space, board)
        if self._side == WHITE:
            self._symbol =  u"♔"
            self._directions = ["nw", "n", "ne", "e", "se", "s", "sw", "w"]
        if self._side == BLACK:
            self._symbol =  u"♚"
            self._directions = ["nw", "n", "ne", "e", "se", "s", "sw", "w"]
        self.type = "ki"
        self.value = 100


    def enumerate_moves(self):
        moves = ChessMoveSet()
        for direction in self._directions:
            one_step = self._board.get_dir(self._current_space, direction)
            if one_step and one_step.is_free():
                m = ChessMove(self._current_space, one_step)
                moves.append(m)
            elif one_step and not one_step.is_free():
                if one_step._piece._side != self._side:
                    m = ChessMove(self._current_space, one_step, [one_step])
                    moves.append(m)
        return moves
