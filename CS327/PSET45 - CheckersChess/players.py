import random
from game_state_chess import ChessGameState
from math import inf
from constants import BLACK, WHITE


class Player:
    "Abstract player class"

    def __init__(self, side=None, depth = 0) -> None:
        self.side = side
        self.depth = depth
        seed = str(open('seed.txt'))
        random.seed(seed)

    def take_turn(self):
        raise NotImplementedError()

    @staticmethod
    def create_player(player_type):
    #    print(player_type[:7])
        "Factory method for creating players"
        if player_type == "human":
            return HumanPlayer()
        elif player_type == "random":
            return RandomCompPlayer()
        elif player_type == "greedy":
            return GreedyCompPlayer()
        elif player_type[:7] == "minimax":
            return MinimaxPlayer(depth = int(player_type[7:]))
        else:
            return None


class HumanPlayer(Player):
    "Concrete player class that prompts for moves via the command line"

    def take_turn(self, game_state):
        b = game_state.board
        while True:
            chosen_piece = input("Select a piece to move\n")
            chosen_piece = b.get_space(chosen_piece).piece
            if chosen_piece is None:
                print("no piece at that location")
                continue
            if chosen_piece.side != self.side:
                print("that is not your piece")
                continue
            options = chosen_piece.enumerate_moves()
            if len(options) == 0 or options[0] not in game_state.all_possible_moves():

                print("that piece cannot move")
                continue

            self._prompt_for_move(options).execute(game_state)
            return

    def _prompt_for_move(self, options):
        while True:
            for idx, op in enumerate(options):
                print(f"{idx}: {op}")
            chosen_move = input(
                "Select a move by entering the corresponding index\n")
            try:
                chosen_move = options[int(chosen_move)]
                return chosen_move
            except ValueError:
                print("not a valid option")


class RandomCompPlayer(Player):
    "Concrete player class that picks random moves"

    def take_turn(self, game_state):
        options = game_state.all_possible_moves()
        m = random.choice(options)
        print(m)
        m.execute(game_state)


class GreedyCompPlayer(Player):
    "Concrete player class that chooses moves that capture the most pieces while breaking ties randomly"

    def take_turn(self, game_state):
        options = game_state.all_possible_moves()
        max_captures = 0
        potential_moves = []
        for m in options:
            if m.num_captures() > max_captures:
                potential_moves = [m]
                max_captures = m.num_captures()
            elif m.num_captures() == max_captures:
                potential_moves.append(m)

        selected_move = random.choice(potential_moves)
        print(selected_move)
        selected_move.execute(game_state)

class MinimaxPlayer(Player):


    def take_turn(self, game_state):
        total_moves = game_state.all_possible_moves(self.side)
        #print(total_moves)

        current_score = -9999
        winning_move = None

        if len(total_moves) > 1:
            for move in total_moves:
                move.execute(game_state)
                score = self.minimax(game_state, self.depth - 1, -9999, 9999)
                move.undo(game_state)
                if score > current_score:
                    winning_move = move
                    current_score = score
        else:
            winning_move = total_moves[0]

        print(winning_move)
        winning_move.execute(game_state)

    def minimax(self, game_state, depth, min, max):

        total_moves = game_state.all_possible_moves()

        total_moves_length = len(total_moves)
        eval = self.evaluate(game_state)

        if total_moves_length == 0 or depth == 0 or eval == -9999 or eval == 9999:
            return eval
        if self.side == game_state.current_side:
            best_move_yet = min
            for move in total_moves:
                move.execute(game_state)
                current_move = self.minimax(game_state, depth - 1, best_move_yet, max)
                move.undo(game_state)
                if current_move > best_move_yet:
                    best_move_yet = current_move
                if best_move_yet > max:
                    return max
            return best_move_yet
        else:
            best_move_yet = max
            for move in total_moves:
                move.execute(game_state)
                current_move = self.minimax(game_state, depth - 1, min, best_move_yet)
                move.undo(game_state)
                if current_move < best_move_yet:
                    best_move_yet = current_move
                if best_move_yet < min:
                    return min
            return best_move_yet

    def evaluate(self, game_state):
        if game_state.check_loss():
            if game_state.current_side != self.side:
                return 9999
            else:
                return -9999
        #
        if game_state.check_draw():
            return 0

        pieces = game_state.all_pieces()

        player1 = self.piece_values(self.side, pieces)
        if self.side == WHITE:
            player2 = self.piece_values(BLACK, pieces)
        else:
            player2 = self.piece_values(WHITE, pieces)

        final_score = player1 - player2

        return final_score

    def piece_values(self, side, pieces):
        total = 0
        for piece in pieces:
            if piece._side == self.side:
                total += piece.value
        return total
