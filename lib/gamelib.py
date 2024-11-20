DEFAULT_ROWS_NUM = 6
DEFAULT_COLUMNS_NUM = 7
PATTERN_LENGTH = 4
DISCS_MAPPING = [' ', '○', '●']

class GameBoard():
    def __init__(self, rows=DEFAULT_ROWS_NUM, columns=DEFAULT_COLUMNS_NUM):
        if not isinstance(rows, int) or rows <= 0:
            raise ValueError("rows must be a positive integer")
        if not isinstance(columns, int) or columns <= 0:
            raise ValueError("columns must be a positive integer")
        self.board = [[0 for _ in range(columns)] for _ in range(rows)]
        self.rows = rows
        self.columns = columns

    def print_board(self) -> None:
        printable_board = []
        for row in self.board:
            printable_row = [DISCS_MAPPING[i] for i in row]
            printable_board.append(printable_row)

        for row in printable_board:
             print(" ".join(row))
        print("-"*self.columns*2)
        print(" ".join(map(str, list(range(self.columns)))))

    def is_column_full(self, column_number:int) -> bool:
        column = [self.board[i][column_number] for i in range(self.rows)]
        if all(element != 0 for element in column):
            return True
        return False

    def is_board_full(self) -> bool:
        return all(cell != 0 for row in self.board for cell in row)

    def make_move(self, column_number: int, player_id: int) -> bool:
        for row in range(self.rows-1, -1, -1):
            if self.board[row][column_number] == 0:
                self.board[row][column_number] = player_id
                return True
        return False

    def _completed_pattern(self, pattern: list, player_id: int) -> bool:
        return all(x == player_id for x in pattern)

    def _check_horizontal_win(self, player_id:int )-> bool:
        """
        Check for horizontal winning combinations. Starting from the
        bottom rows
        """
        for row in range(self.rows-1, 0, -1):
            for column in range(self.columns-PATTERN_LENGTH-1):
                horizontal = self.board[row][column:column+PATTERN_LENGTH]
                if self._completed_pattern(horizontal, player_id):
                    return True
        return False

    def _check_vertical_win(self, player_id: int) -> bool:
        """
        Check for vertical winning combinations. Starting from the
        bottom rows
        """
        for row in range(self.rows-1, PATTERN_LENGTH-2, -1):
            for column in range(self.columns):
                vertical = [self.board[row-i][column] for i in range(PATTERN_LENGTH)]
                if self._completed_pattern(vertical, player_id):
                    return True
        return False


    def _check_sloped_win(self, player_id: int) -> bool:
        """
        Check for sloped winning combinations. Starting from the
        bottom rows
        """
        for row in range(self.rows-1, -1, -1):
            for column in range(self.columns):
                #
                if row - PATTERN_LENGTH + 1 >= 0 and column + PATTERN_LENGTH <= self.columns:
                    slope = [self.board[row-i][column+i] for i in range(PATTERN_LENGTH)]
                    if self._completed_pattern(slope, player_id):
                        return True

                if row - PATTERN_LENGTH + 1 >= 0 and column - PATTERN_LENGTH + 1 >= 0:
                    slope = [self.board[row-i][column-i] for i in range(PATTERN_LENGTH)]
                    if self._completed_pattern(slope, player_id):
                        return True
        return False

    def check_for_win(self, player_id: int) -> bool:
        return any(check for check in [self._check_horizontal_win(player_id),
                                         self._check_vertical_win(player_id),
                                         self._check_sloped_win(player_id)])

class Player():
    _counter = 0

    def __init__(self, player_name)->None:
        if not isinstance(player_name, str) or not player_name.strip():
            raise ValueError("Player name must be a non-empty string")

        if Player._counter >= 2:
            raise ValueError("Only two players could exist in the game")
        Player._counter += 1

        self.id = Player._counter
        self.name = player_name
        self.winner = False

    def drop_disc(self, board: GameBoard)->None:
        while True:
            print(f"It's {self.name}'s turn")
            try:
                column = int(input("Select the column number 0-6: "))
                if 0 <= column < board.columns:
                    if board.make_move(column, self.id):
                        print("Next move")
                        return
                    else:
                        print("The column is full. Choose another one")
                        self.drop_disc(board)
                else:
                    print("Invalid column number. Choose a number between 0 and 6")
            except ValueError:
                print("Invalid input. Enter a number between 0 and 6")

    @classmethod
    def reset_counter(cls: type('Player')) -> None:
        """
        Resets the player counter. For testing purposes or for restarting the game
        """
        cls._counter = 0
