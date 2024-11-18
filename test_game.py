import pytest
from lib.gamelib import GameBoard, Player

DEFAULT_ROWS_NUM = 6
DEFAULT_COLUMNS_NUM = 7
PATTERN_LENGTH = 4


def test_gameboard_initialization():
    board = GameBoard()
    assert board.rows == DEFAULT_ROWS_NUM
    assert board.columns == DEFAULT_COLUMNS_NUM
    assert len(board.board) == DEFAULT_ROWS_NUM
    assert len(board.board[0]) == DEFAULT_COLUMNS_NUM

    board = GameBoard(rows=5, columns=8)
    assert board.rows == 5
    assert board.columns == 8
    assert len(board.board) == 5
    assert len(board.board[0]) == 8

    with pytest.raises(ValueError):
        GameBoard(rows=-1, columns=7)
    with pytest.raises(ValueError):
        GameBoard(rows=6, columns="invalid")

def test_gameboard_make_move():
    board = GameBoard()
    assert board.make_move(0, 1)
    assert board.board[-1][0] == 1
    assert board.make_move(0, 2)
    assert board.board[-2][0] == 2

    for _ in range(DEFAULT_ROWS_NUM - 2):
        board.make_move(0, 1)
    assert not board.make_move(0, 1)

def test_gameboard_is_column_full():
    board = GameBoard(rows=3, columns=3)
    for i in range(3):
        board.make_move(0, 1)
    #assert board.is_column_full(0)
    assert not board.is_column_full(1)

def test_gameboard_is_board_full():
    board = GameBoard(rows=2, columns=2)
    assert not board.is_board_full()
    for i in range(2):
        for j in range(2):
            board.make_move(j, 1)
    assert board.is_board_full()

def test_gameboard_check_for_win():
    board = GameBoard(rows=6, columns=7)

    for col in range(PATTERN_LENGTH):
        board.make_move(col, 1)
    assert board.check_for_win(1)

    board = GameBoard(rows=6, columns=7)
    for _ in range(PATTERN_LENGTH):
        board.make_move(0, 2)
    assert board.check_for_win(2)

    board = GameBoard(rows=4, columns=4)
    board.make_move(0, 1)
    board.make_move(1, 2)
    board.make_move(1, 1)
    board.make_move(2, 2)
    board.make_move(2, 2)
    board.make_move(2, 1)
    board.make_move(3, 2)
    board.make_move(3, 2)
    board.make_move(3, 2)
    board.make_move(3, 1)
    assert board.check_for_win(1)


def test_player_initialization():
    Player.reset_counter()
    player1 = Player("Alice")
    player2 = Player("Bob")
    assert player1.id == 1
    assert player1.name == "Alice"
    assert player2.id == 2
    assert player2.name == "Bob"

    with pytest.raises(ValueError):
        Player("")
    with pytest.raises(ValueError):
        Player(" ")
    with pytest.raises(ValueError):
        Player("Charlie")

def test_player_reset_counter():
    Player.reset_counter()
    Player("Alice")
    Player("Bob")
    Player.reset_counter()
    player1 = Player("Charlie")
    assert player1.id == 1

def test_player_drop_disc(monkeypatch):
    Player.reset_counter()
    player = Player("Alice")
    board = GameBoard()

    # Simulate user input
    inputs = iter(["0", "6", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    player.drop_disc(board)
    assert board.board[-1][0] == player.id