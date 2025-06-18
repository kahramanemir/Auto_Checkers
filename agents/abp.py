import copy
import math

class ABPPlayer:
    def __init__(self, color, depth=3):
        self.color = color
        self.depth = depth

    def get_move(self, board):
        best_score, best_move = self.minimax(board, self.depth, True, -math.inf, math.inf)
        if best_move:
            sr, sc = best_move[0]
            er, ec = best_move[1]
            temp_board = copy.deepcopy(board)
            jumped, (new_r, new_c) = temp_board.move_piece((sr, sc), (er, ec))
            if jumped:
                while True:
                    more_jumps = temp_board.get_valid_moves(new_r, new_c, only_captures=True)
                    if not more_jumps:
                        break
                    jump_to = self.select_best_jump(temp_board, new_r, new_c, more_jumps)
                    temp_board.move_piece((new_r, new_c), jump_to)
                    new_r, new_c = jump_to
            return ((sr, sc), (er, ec))
        return None

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        winner = board.check_winner()
        if depth == 0 or winner is not None:
            return self.evaluate(board), None

        color = self.color if maximizing_player else ("b" if self.color == "w" else "w")
        best_move = None
        moves = board.get_all_moves(color)

        if maximizing_player:
            max_eval = -math.inf
            for move in moves:
                temp_board = copy.deepcopy(board)
                temp_board.move_piece(*move)
                eval_score, _ = self.minimax(temp_board, depth - 1, False, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in moves:
                temp_board = copy.deepcopy(board)
                temp_board.move_piece(*move)
                eval_score, _ = self.minimax(temp_board, depth - 1, True, alpha, beta)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate(self, board):
        score = 0
        for row in board.board:
            for piece in row:
                if piece != 0:
                    base_score = 5 if piece.isupper() else 1
                    if piece.lower() == self.color:
                        score += base_score
                    else:
                        score -= base_score
        return score

    def select_best_jump(self, board, r, c, jump_options):
        max_captures = -1
        best_jump = jump_options[0]
        for jump in jump_options:
            temp = copy.deepcopy(board)
            temp.move_piece((r, c), jump)
            count = self.count_additional_jumps(temp, jump[0], jump[1])
            if count > max_captures:
                max_captures = count
                best_jump = jump
        return best_jump

    def count_additional_jumps(self, board, r, c):
        total = 0
        while True:
            next_jumps = board.get_valid_moves(r, c, only_captures=True)
            if not next_jumps:
                break
            total += 1
            r, c = next_jumps[0]
        return total