# ♟️ Auto Checkers – AI-Powered Checkers Game

Auto Checkers is an automated checkers game where AI agents compete using different algorithms. You can customize which AI controls each player and adjust their parameters to observe performance differences.

## 🚀 Features

- AI algorithm selection for both White and Black players
- Supports ABP (Alpha-Beta Pruning), MCTS, and Random AI
- Configurable AI parameters (depth, simulations, etc.)
- Parallel simulation of up to 9 games
- Visual game board using Pygame
- AI configuration menu using DearPyGui
- Displays game result and simulation time

## 📁 Project Structure

```
AI_Odev/
├── main.py              # Main game loop and window management
├── menu.py              # AI configuration menu (DearPyGui)
├── constants.py         # Global constants (e.g., screen size, FPS)
├── board.py             # Game logic and board representation
├── agents/              # All AI player implementations
│   ├── abp.py           # Alpha-Beta Pruning algorithm
│   ├── mcts.py          # Monte Carlo Tree Search algorithm
│   └── random.py        # Random move selector
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 🔧 Setup

Clone or download the project:

```
git clone https://github.com/kahramanemir/Auto_Checkers.git
cd Auto_Checkers
```

Create a virtual environment and install dependencies:

```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Running the Game

Run the game with:

```
python main.py
```

- An AI configuration menu will appear.
- Choose AI types and adjust their parameters.
- Click "Start Game" to launch the Pygame game window.

## 🤖 Supported AI Algorithms

| AI Type          | Description                     | Parameter              |
| ---------------- | ------------------------------- | ---------------------- |
| ABP (Alpha-Beta) | Minimax with alpha-beta pruning | Search Depth (1–5)     |
| MCTS             | Monte Carlo Tree Search         | Simulations (100–2000) |
| Random           | Picks a valid move randomly     | None                   |

## ⚠️ Notes

- High parameter values may significantly slow down gameplay or overload the system.

## 👤 Developers

**Emir Kahraman**\
**Bülent Yıldırım**

