import pygame
import random
import time
from menu import show_ai_menu
from constants import *
from board import Board
from agents.minmax import MINMAXPlayer
from agents.mcts import MCTSPlayer

NUM_GAMES = 1
ROWS, COLS = 1, 1
SUB_WIDTH = WIDTH // COLS
SUB_HEIGHT = HEIGHT // ROWS

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Parallel Checkers")

class GameInstance:
    def __init__(self, x_idx, y_idx, minimax_depth=3, mcts_simulations=500):
        self.x_idx = x_idx
        self.y_idx = y_idx
        self.minimax_depth = minimax_depth
        self.mcts_simulations = mcts_simulations
        self.reset()

    def reset(self):
        self.board = Board()
        self.white_ai = MINMAXPlayer("w", depth=self.minimax_depth)
        self.black_ai = MCTSPlayer("b", simulations=self.mcts_simulations)
        self.current_turn = random.choice(["w", "b"])
        self.finished = False
        self.winner = None
        self.start_time = time.time()
        self.last_move = []

    def update(self):
        if self.finished:
            return

        move = None
        if self.current_turn == "w":
            move = self.white_ai.get_move(self.board)
        else:
            move = self.black_ai.get_move(self.board)

        if move:
            jumped, _ = self.board.move_piece(*move)
            self.last_move = self.board.last_move
            self.current_turn = "b" if self.current_turn == "w" else "w"
        else:
            self.finished = True
            self.winner = "Black" if self.current_turn == "w" else "White"

    def draw(self, win):
        surface = pygame.Surface((SUB_WIDTH, SUB_HEIGHT))
        self.board.draw(surface, last_move=self.last_move)

        if self.finished:
            overlay = pygame.Surface((SUB_WIDTH, SUB_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))

            font = pygame.font.SysFont("arial", 24, bold=True)
            text = font.render(f"{self.winner} wins!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SUB_WIDTH // 2, SUB_HEIGHT // 2))
            surface.blit(text, text_rect)
        
        font = pygame.font.SysFont("arial", 20)
        turn_text = font.render(f"Turn: {'White' if self.current_turn == 'w' else 'Black'}", True, (255, 255, 255))
        surface.blit(turn_text, (10, 10))
        
        pygame.draw.rect(surface, (200, 200, 200), surface.get_rect(), 2)
        win.blit(surface, (self.x_idx * SUB_WIDTH, self.y_idx * SUB_HEIGHT))
    

def main():
    params = show_ai_menu()
    minimax_depth = params["minimax_depth"]
    mcts_simulations = params["mcts_simulations"]
    num_games = params["num_games"]

    global NUM_GAMES, ROWS, COLS, SUB_WIDTH, SUB_HEIGHT
    NUM_GAMES = num_games
    ROWS = COLS = int(num_games ** 0.5) + (0 if int(num_games ** 0.5) ** 2 == num_games else 1)
    SUB_WIDTH = WIDTH // COLS
    SUB_HEIGHT = HEIGHT // ROWS


    pygame.init()
    clock = pygame.time.Clock()
    games = []

    for i in range(NUM_GAMES):
        x = i % COLS
        y = i // COLS
        game = GameInstance(x, y, minimax_depth, mcts_simulations)
        games.append(game)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        all_finished = True
        WIN.fill((0, 0, 0))

        for game in games:
            if not game.finished and (time.time() - game.start_time > 90):
                game.reset()

            game.update()
            game.draw(WIN)

            if not game.finished:
                all_finished = False

        pygame.display.update()

        if all_finished:
            pygame.time.wait(1000)
            run = False

    pygame.quit()

if __name__ == "__main__":
    main()