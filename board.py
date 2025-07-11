import pygame
import math
import time
from constants import *

class Board:
    def __init__(self):
        self.board = []
        self.last_move = []
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row in [1, 2]:
                    self.board[row].append("b")
                elif row in [5, 6]:
                    self.board[row].append("w")
                else:
                    self.board[row].append(0)

    def draw(self, surface, last_move=None):
        if last_move is None:
            last_move = self.last_move
        height, width = surface.get_height(), surface.get_width()
        square_size = min(width, height) // ROWS

        surface.fill(DARK_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(surface, LIGHT_BROWN,
                                 (col * square_size, row * square_size, square_size, square_size))

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    color = BLACK if piece.lower() == "b" else WHITE
                    center = (col * square_size + square_size // 2, row * square_size + square_size // 2)
                    radius = square_size // 2 - 4
                    pygame.draw.circle(surface, color, center, radius)

                    if piece.isupper():
                        font = pygame.font.SysFont(None, square_size // 2)
                        text_color = WHITE if color == BLACK else BLACK
                        text = font.render("K", True, text_color)
                        surface.blit(text, (center[0] - text.get_width() // 2,
                                            center[1] - text.get_height() // 2))

        if last_move:
            for move in last_move:
                sr, sc = move[0]
                er, ec = move[1]
                start_pos = (sc * square_size + square_size // 2, sr * square_size + square_size // 2)
                end_pos = (ec * square_size + square_size // 2, er * square_size + square_size // 2)

                arrow_color = (255, 0, 0)
                pygame.draw.line(surface, arrow_color, start_pos, end_pos, 3)

                dx, dy = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
                angle = math.atan2(dy, dx)
                arrow_length = 12
                tip = end_pos
                left = (tip[0] - arrow_length * math.cos(angle - math.pi / 6),
                        tip[1] - arrow_length * math.sin(angle - math.pi / 6))
                right = (tip[0] - arrow_length * math.cos(angle + math.pi / 6),
                         tip[1] - arrow_length * math.sin(angle + math.pi / 6))
                pygame.draw.polygon(surface, arrow_color, [tip, left, right])

    def is_within_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_valid_moves(self, row, col, only_captures=False):
        moves = []
        piece = self.board[row][col]
        if piece == 0:
            return moves

        if piece.isupper():
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                jumped = False
                r, c = row + dr, col + dc
                while self.is_within_bounds(r, c):
                    target = self.board[r][c]
                    if target == 0 and not jumped:
                        if not only_captures:
                            moves.append((r, c))
                    elif target != 0 and target.lower() != piece.lower() and not jumped:
                        jumped = True
                    elif target == 0 and jumped:
                        moves.append((r, c))
                        break
                    else:
                        break
                    r += dr
                    c += dc
        else:
            directions = [(-1, 0), (0, -1), (0, 1)] if piece == "w" else [(1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if self.is_within_bounds(new_row, new_col):
                    target = self.board[new_row][new_col]
                    if target == 0 and not only_captures:
                        moves.append((new_row, new_col))
                    elif target != 0 and target.lower() != piece.lower():
                        jump_row, jump_col = new_row + dr, new_col + dc
                        if self.is_within_bounds(jump_row, jump_col) and self.board[jump_row][jump_col] == 0:
                            moves.append((jump_row, jump_col))
        return moves

    def get_all_moves(self, color):
        all_moves = []
        must_jump = []

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0 and self.board[row][col].lower() == color:
                    captures = self.get_valid_moves(row, col, only_captures=True)
                    if captures:
                        for move in captures:
                            must_jump.append(((row, col), move))
                    else:
                        moves = self.get_valid_moves(row, col)
                        for move in moves:
                            all_moves.append(((row, col), move))

        return must_jump if must_jump else all_moves

    def move_piece(self, start, end):
        self.last_move = []  # Her hamle başında sıfırla
        sr, sc = start
        er, ec = end
        piece = self.board[sr][sc]
        self.board[sr][sc] = 0
        self.board[er][ec] = piece
        self.last_move.append(((sr, sc), (er, ec)))

        jumped = False
        if abs(er - sr) > 1 or abs(ec - sc) > 1:
            jumped = True
            dr = (er - sr) // max(1, abs(er - sr)) if er != sr else 0
            dc = (ec - sc) // max(1, abs(ec - sc)) if ec != sc else 0
            r, c = sr + dr, sc + dc
            while r != er or c != ec:
                if self.board[r][c] != 0 and self.board[r][c].lower() != piece.lower():
                    self.board[r][c] = 0
                    break
                r += dr
                c += dc

        if piece == "w" and er == 0:
            self.board[er][ec] = "W"
        elif piece == "b" and er == 7:
            self.board[er][ec] = "B"

        while jumped:
            more_jumps = self.get_valid_moves(er, ec, only_captures=True)
            if not more_jumps:
                break

            next_r, next_c = more_jumps[0]
            sr, sc = er, ec
            er, ec = next_r, next_c
            self.board[sr][sc] = 0
            self.board[er][ec] = piece
            self.last_move.append(((sr, sc), (er, ec)))
            dr = (er - sr) // max(1, abs(er - sr)) if er != sr else 0
            dc = (ec - sc) // max(1, abs(ec - sc)) if ec != sc else 0
            r, c = sr + dr, sc + dc
            while r != er or c != ec:
                if self.board[r][c] != 0 and self.board[r][c].lower() != piece.lower():
                    self.board[r][c] = 0
                    break
                r += dr
                c += dc
            if piece == "w" and er == 0:
                self.board[er][ec] = "W"
            elif piece == "b" and er == 7:
                self.board[er][ec] = "B"

        return jumped, (er, ec)

    def check_winner(self):
        whites = [p for row in self.board for p in row if p != 0 and p.lower() == 'w']
        blacks = [p for row in self.board for p in row if p != 0 and p.lower() == 'b']

        white_moves = any(self.get_valid_moves(row, col)
                          for row in range(ROWS) for col in range(COLS)
                          if self.board[row][col] != 0 and self.board[row][col].lower() == 'w')
        black_moves = any(self.get_valid_moves(row, col)
                          for row in range(ROWS) for col in range(COLS)
                          if self.board[row][col] != 0 and self.board[row][col].lower() == 'b')

        if not whites or not white_moves:
            return "b"
        if not blacks or not black_moves:
            return "w"

        return None