# NIM GAME — Minimax vs Alpha-Beta

A graphical Nim game built with **Pygame** that pits a human player against an AI. The AI uses **Alpha-Beta Pruning** to make its moves, while both **Minimax** and **Alpha-Beta** run every turn so you can compare their performance side by side.

## What is Nim?

Nim is a two-player strategy game where players take turns removing stones from heaps. The player who takes the **last stone loses** (misère convention).

## Features

- 5 difficulty levels (Easy → Master) with increasing heap sizes and search depth
- AI uses Alpha-Beta Pruning for optimal play
- Real-time stats panel comparing Minimax vs Alpha-Beta (time, nodes visited, max depth)
- Pruning savings badge showing how many nodes Alpha-Beta skipped
- Particle effects on stone removal
- Dynamic level progression — win to go up, lose to go down

## Difficulty Levels

| Level  | Heaps     | Max Depth |
|--------|-----------|-----------|
| Easy   | [2, 3]    | 4         |
| Normal | [3, 4, 5] | 6         |
| Hard   | [4, 5, 6] | 7         |
| Expert | [3, 5, 7] | 7         |
| Master | [4, 6, 8] | 8         |

## Requirements

- Python 3.x
- Pygame

```bash
pip install pygame
```

## Font

The game uses **VCR OSD Mono** for its retro aesthetic. If the font is not installed, Pygame will fall back to the system default font automatically.

To install it manually:
1. Download **VCR OSD Mono** from [DaFont](https://www.dafont.com/vcr-osd-mono.font)
2. Extract the `.ttf` file
3. Install it:
   - **Windows**: Right-click the `.ttf` file → *Install*
   - **macOS**: Double-click the `.ttf` file → *Install Font*
   - **Linux**: Copy the `.ttf` file to `~/.fonts/` then run `fc-cache -fv`

## How to Run

```bash
python "Nim Game.py"
```

## How to Play

1. Click a **heap** to select it
2. Click a **number button** to remove that many stones from the selected heap
3. The AI responds automatically after your move
4. The player who takes the **last stone loses**

## Controls

| Button       | Action                                      |
|--------------|---------------------------------------------|
| NEW GAME     | Restart at the current level                |
| RUN BOTH NOW | Manually trigger both algorithms to compare |
| NEXT LEVEL   | Jump to the next difficulty                 |
| PREV LEVEL   | Go back to the previous difficulty          |

## Project Structure

```
Nim Game.py       # Main file — game logic, AI, and rendering
```

## AI Implementation

Both algorithms use a **Nim-value heuristic** (XOR of heap sizes) at the depth cutoff:
- `minimax()` — plain Minimax, runs for stats only
- `alphabeta()` — Alpha-Beta Pruning, used for the AI's actual move decision
