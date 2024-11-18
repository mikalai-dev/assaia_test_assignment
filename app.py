"""
Title: Connect 4 Game Implementation
Author: Mikalai H
Date: November 18, 2024
Version: 1.0.0
Description:

Author Contact:
    Email: contact@mikalai.info
    GitHub: https://github.com/mikalai-dev
    LinkedIn: https://www.linkedin.com/in/mikalai-hrytsuk

Usage:
    Run the script directly to play the game in the console:
    $ python3 app.py

License:
    MIT License - Free to use, modify, and distribute with proper attribution.
"""

from lib.gamelib import GameBoard, Player

def main():
    board = GameBoard(6, 7)
    player1_name = input("Enter the name for the first player: ")
    player1 = Player(player1_name)
    player2_name = input("Enter the name for the second player: ")
    player2 = Player(player2_name)

    while True:
        for player in [player1, player2]:
            player.drop_disc(board)
            board.print_board()
            if board.check_for_win(player.id):
                print("---------------------------------------")
                print(f"The Winner is {player.name}    !!!")
                print("---------------------------------------")
                board.print_board()
                return
            if board.is_board_full():
                print("The game is a draw")
                return

if __name__ == '__main__':
    main()
