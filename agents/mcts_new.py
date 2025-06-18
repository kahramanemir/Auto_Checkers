# Updated mcts.py
import copy
import random
import math

class MCTSNode:
    def __init__(self, board, color, parent=None, move=None):
        self.board = board
        self.color = color  # Player to move *after* this node's move
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0

    def get_untried_moves(self):
        all_moves = self.board.get_all_moves(self.color)
        tried_moves = [child.move for child in self.children]
        return [move for move in all_moves if move not in tried_moves]

    def is_fully_expanded(self):
        return len(self.get_untried_moves()) == 0

    def best_child(self, c_param=1.4):
        return max(self.children, key=lambda child:
                   (child.wins / (child.visits + 1e-6)) +
                   c_param * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6)))

class MCTSPlayer:
    def __init__(self, color, simulations=100, exploration_constant=1.4):
        self.color = color
        self.simulations = simulations
        self.c_param = exploration_constant

    def get_move(self, board):
        root = MCTSNode(copy.deepcopy(board), self.color)

        for _ in range(self.simulations):
            node = root

            # Selection
            while node.children and node.is_fully_expanded():
                node = node.best_child(self.c_param)

            # Expansion
            untried_moves = node.get_untried_moves()
            if untried_moves:
                move = random.choice(untried_moves)
                temp_board = copy.deepcopy(node.board)
                jumped, (r, c) = temp_board.move_piece(*move)

                # Handle chained jumps
                if jumped:
                    while True:
                        more_jumps = temp_board.get_valid_moves(r, c, only_captures=True)
                        if not more_jumps:
                            break
                        jump_to = random.choice(more_jumps)
                        jumped, (r, c) = temp_board.move_piece((r, c), jump_to)

                next_color = "b" if node.color == "w" else "w"
                child = MCTSNode(temp_board, next_color, parent=node, move=move)
                node.children.append(child)
                node = child

            # Simulation (from the opponent's turn)
            sim_start_color = "b" if node.color == "w" else "w"
            winner = self.simulate_random_game(node.board, sim_start_color)

            # Backpropagation
            self.backpropagate(node, winner)

        if not root.children:
            return None

        best_move = max(root.children, key=lambda c: c.visits).move
        return best_move

    def simulate_random_game(self, board, color):
        temp_board = copy.deepcopy(board)
        current_color = color
        turn_limit = 100

        for _ in range(turn_limit):
            winner = temp_board.check_winner()
            if winner is not None:
                return winner

            moves = temp_board.get_all_moves(current_color)
            if not moves:
                return "b" if current_color == "w" else "w"

            move = random.choice(moves)
            jumped, (r, c) = temp_board.move_piece(*move)

            if jumped:
                while True:
                    more_jumps = temp_board.get_valid_moves(r, c, only_captures=True)
                    if not more_jumps:
                        break
                    jump_to = random.choice(more_jumps)
                    jumped, (r, c) = temp_board.move_piece((r, c), jump_to)

            current_color = "b" if current_color == "w" else "w"

        return None  # draw or unresolved

    def backpropagate(self, node, winner):
        while node is not None:
            node.visits += 1
            if winner == self.color:
                node.wins += 1
            node = node.parent