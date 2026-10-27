#include <iostream>
#include <algorithm>
#include <bits/stdc++.h>
#include <limits>
using namespace std;

#define Grid_Size 3

class Game {
private:
    char grid[Grid_Size][Grid_Size];

public:
    Game() {
        reset();
    }

    void reset() {
        for (int i = 0; i < Grid_Size; i++) {
            for (int j = 0; j < Grid_Size; j++) {
                grid[i][j] = ' ';
            }
        }
    }

    void display() {
        cout << "\n";
        for (int i = 0; i < Grid_Size; i++) {
            for (int j = 0; j < Grid_Size; j++) {
                cout << (grid[i][j] == ' ' ? char('1' + i * 3 + j) : grid[i][j]);
                if (j < 2) cout << " | ";
            }
            cout << "\n";
            if (i < 2) cout << "--+---+--\n";
        }
        cout << "\n";
    }

    bool isMovesLeft() {
        for (int i = 0; i < Grid_Size; i++)
            for (int j = 0; j < Grid_Size; j++)
                if (grid[i][j] == ' ')
                    return true;
        return false;
    }

    int evaluate() {
        // Rows, Columns, Diagonals
        for (int row = 0; row < 3; row++) {
            if (grid[row][0] == grid[row][1] &&
                grid[row][1] == grid[row][2] &&
                grid[row][0] != ' ')
                return (grid[row][0] == 'O') ? +10 : -10;
        }

        for (int col = 0; col < 3; col++) {
            if (grid[0][col] == grid[1][col] &&
                grid[1][col] == grid[2][col] &&
                grid[0][col] != ' ')
                return (grid[0][col] == 'O') ? +10 : -10;
        }

        if (grid[0][0] == grid[1][1] &&
            grid[1][1] == grid[2][2] &&
            grid[0][0] != ' ')
            return (grid[0][0] == 'O') ? +10 : -10;

        if (grid[0][2] == grid[1][1] &&
            grid[1][1] == grid[2][0] &&
            grid[0][2] != ' ')
            return (grid[0][2] == 'O') ? +10 : -10;

        return 0;
    }

    int minimax(int depth, bool isMax) {
        int score = evaluate();

        if (score == 10) return score - depth;
        if (score == -10) return score + depth;
        if (!isMovesLeft()) return 0;

        if (isMax) {
            int best = -1000;
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    if (grid[i][j] == ' ') {
                        grid[i][j] = 'O';
                        best = max(best, minimax(depth + 1, false));
                        grid[i][j] = ' ';
                    }
                }
            }
            return best;
        } else {
            int best = 1000;
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    if (grid[i][j] == ' ') {
                        grid[i][j] = 'X';
                        best = min(best, minimax(depth + 1, true));
                        grid[i][j] = ' ';
                    }
                }
            }
            return best;
        }
    }

    void bestMove() {
        int bestVal = -1000;
        int bestRow = -1, bestCol = -1;

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (grid[i][j] == ' ') {
                    grid[i][j] = 'O';
                    int moveVal = minimax(0, false);
                    grid[i][j] = ' ';

                    if (moveVal > bestVal) {
                        bestRow = i;
                        bestCol = j;
                        bestVal = moveVal;
                    }
                }
            }
        }

        grid[bestRow][bestCol] = 'O';
    }

    bool makeMove(int pos, char player) {
        int row = (pos - 1) / 3;
        int col = (pos - 1) % 3;

        if (grid[row][col] != ' ') return false;

        grid[row][col] = player;
        return true;
    }

    bool checkWin(char player) {
        for (int i = 0; i < 3; i++) {
            if (grid[i][0] == player && grid[i][1] == player && grid[i][2] == player)
                return true;
            if (grid[0][i] == player && grid[1][i] == player && grid[2][i] == player)
                return true;
        }

        if (grid[0][0] == player && grid[1][1] == player && grid[2][2] == player)
            return true;
        if (grid[0][2] == player && grid[1][1] == player && grid[2][0] == player)
            return true;

        return false;
    }
};

int main() {
    Game game;
    int move;

    cout << "Tic Tac Toe (You = X, AI = O)\n";

    while (true) {
        game.display();

        // Player move
        cout << "Enter your move (1-9): ";
        cin >> move;

        if (!game.makeMove(move, 'X')) {
            cout << "Invalid move!\n";
            continue;
        }

        if (game.checkWin('X')) {
            game.display();
            cout << "You win!\n";
            break;
        }

        if (!game.isMovesLeft()) {
            game.display();
            cout << "Draw!\n";
            break;
        }

        // AI move
        game.bestMove();

        if (game.checkWin('O')) {
            game.display();
            cout << "AI wins!\n";
            break;
        }

        if (!game.isMovesLeft()) {
            game.display();
            cout << "Draw!\n";
            break;
        }
    }

    return 0;
}