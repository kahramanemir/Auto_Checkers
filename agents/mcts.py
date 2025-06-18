import copy
import random
import math

class MCTSNode:
    def __init__(self, board, color, parent=None, move=None):
        self.board = board                      # Game state
        self.color = color                      # Who's to move at this node
        self.parent = parent                    # Parent node
        self.move = move                        # Move that led to this node
        self.children = []                      # Child nodes
        self.visits = 0                         # Visit count
        self.wins = 0                           # Win count

    def get_untried_moves(self):
        """Returns legal moves from this node's state that have not yet been explored."""
        all_moves = self.board.get_all_moves(self.color)
        tried_moves = [child.move for child in self.children]
        return [move for move in all_moves if move not in tried_moves]

    def is_fully_expanded(self):
        """True if all possible moves have been tried (i.e., node is fully expanded)."""
        return len(self.get_untried_moves()) == 0

    def best_child(self, c_param=1.4):
        """Selects child with highest UCB1 score."""
        choices_weights = [
            (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

class MCTSPlayer:
    def __init__(self, color, simulations=100, exploration_constant=1.4):
        self.color = color
        self.simulations = simulations
        self.c_param = exploration_constant

    def get_move(self, board):
        root = MCTSNode(copy.deepcopy(board), self.color)

        for _ in range(self.simulations):
            node = root

            # --- Selection ---
            while node.children and node.is_fully_expanded():
                node = node.best_child(self.c_param)

            # --- Expansion ---
            untried_moves = node.get_untried_moves()
            if untried_moves:
                move = random.choice(untried_moves)
                temp_board = copy.deepcopy(node.board)
                temp_board.move_piece(*move)
                next_color = "b" if node.color == "w" else "w"
                child = MCTSNode(temp_board, next_color, parent=node, move=move)
                node.children.append(child)
                node = child

            # --- Simulation ---
            winner = self.simulate_random_game(node.board, node.color)

            # --- Backpropagation ---
            self.backpropagate(node, winner)

        # Choose the child with the most visits as the final move
        if not root.children:
            return None

        best_move = max(root.children, key=lambda c: c.visits).move
        return best_move

    def simulate_random_game(self, board, color):
        temp_board = copy.deepcopy(board)
        current_color = color

        while True:
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


    def backpropagate(self, node, winner):
        """Propagate the result up to the root node."""
        while node is not None:
            node.visits += 1
            if winner == self.color:
                node.wins += 1
            # Optional: handle draws if your game supports them
            # elif winner == "draw":
            #     node.wins += 0.5
            node = node.parent