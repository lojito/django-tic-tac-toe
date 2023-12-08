from .board import Board
from .constants import COMPUTER, SQUARE_NOT_FOUND, USER


class Computer:
    def __init__(
        self,
        board: Board,
    ):
        self._board = board

    def play(self):
        square = self._board.get_winning_square(COMPUTER)
        if square != SQUARE_NOT_FOUND:
            self._board.place(COMPUTER, square)
            return square
        square = self._board.get_winning_square(USER)
        if square != SQUARE_NOT_FOUND:
            self._board.place(COMPUTER, square)
            return square
        square = self._board.place_random_empty_square(COMPUTER)
        if square != SQUARE_NOT_FOUND:
            return square
        else:
            return SQUARE_NOT_FOUND
