import random

class RandomPlayer:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        valid_moves = board.get_all_moves(self.color)
        if not valid_moves:
            return None
        return random.choice(valid_moves)