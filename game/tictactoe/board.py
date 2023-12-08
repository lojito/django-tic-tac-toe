from random import randint

from .constants import (
    COMPUTER,
    NO_PLAYER_YET,
    ROWS_OF_SQUARES,
    SQUARE_NOT_FOUND,
    SQUARES_NUMBER,
    USER,
)
from .exceptions import (
    BoardAlreadyInUseSquareError,
    BoardInvalidError,
    BoardInvalidPlayerError,
    BoardInvalidSquareError,
)


class Board:
    def __init__(self, board):
        if not isinstance(board, str) or len(board) != SQUARES_NUMBER:
            raise BoardInvalidError(board)

        self._squares = []
        for player in board:
            if player not in [NO_PLAYER_YET, USER, COMPUTER]:
                raise BoardInvalidError(board)
            self._squares.append(player)

    @staticmethod
    def check_player(player):
        if player not in (USER, COMPUTER):
            raise BoardInvalidPlayerError(player)

    def is_full(self):
        return NO_PLAYER_YET not in self._squares

    def is_square_empty(self, square):
        return self[square] == NO_PLAYER_YET

    def empty_squares(self):
        return list(
            filter(
                self.is_square_empty,
                range(SQUARES_NUMBER),
            )
        )

    def is_placed_three_times_in_a_row_of_squares(self, player, squares, empty_square):
        return (
            self[squares[0]] == player
            and self[squares[1]] == player
            and self[squares[2]] == player
            and self[empty_square] == NO_PLAYER_YET
        )

    def get_winning_square(self, player):
        Board.check_player(player)

        if self.is_full():
            return SQUARE_NOT_FOUND

        for square1, square2, square3, square4 in ROWS_OF_SQUARES:
            if self.is_placed_three_times_in_a_row_of_squares(
                player, [square1, square2, square3], square4
            ):
                return square4
            if self.is_placed_three_times_in_a_row_of_squares(
                player, [square1, square2, square4], square3
            ):
                return square3
            if self.is_placed_three_times_in_a_row_of_squares(
                player, [square1, square3, square4], square2
            ):
                return square2
            if self.is_placed_three_times_in_a_row_of_squares(
                player, [square2, square3, square4], square1
            ):
                return square1

        return SQUARE_NOT_FOUND

    def won(self, player):
        Board.check_player(player)

        for square1, square2, square3, square4 in ROWS_OF_SQUARES:
            if (
                self[square1] == player
                and self[square2] == player
                and self[square3] == player
                and self[square4] == player
            ):
                return (True, [square1, square2, square3, square4])
        return (False, [])

    def place(self, player, square):
        self[square] = player

    def place_random_empty_square(self, player):
        if self.is_full():
            return SQUARE_NOT_FOUND

        empty_squares = self.empty_squares()
        index = randint(0, len(empty_squares) - 1)
        square = empty_squares[index]
        self.place(player, square)
        return square

    def __getitem__(self, square):
        try:
            return self._squares[square]
        except IndexError as exc:
            raise BoardInvalidSquareError(square) from exc

    def __setitem__(self, square, player):
        Board.check_player(player)

        if not self.is_square_empty(square):
            raise BoardAlreadyInUseSquareError(self, square)

        try:
            self._squares[square] = player
        except IndexError as exc:
            raise BoardInvalidSquareError(square) from exc

    def __str__(self):
        return "".join([player for player in self._squares])
