from abc import ABCMeta, abstractmethod

from .constants import COMPUTER, NO_PLAYER_YET, SQUARES_NUMBER, USER, MESSAGES


class BoardSquareError(Exception, metaclass=ABCMeta):
    def __init__(self, square):
        self._square = square

    @abstractmethod
    def __str__(self):
        pass


class BoardInvalidSquareError(BoardSquareError):
    def __str__(self):
        return MESSAGES["INVALID_POSITION"].format(
            str(self._square), SQUARES_NUMBER - 1
        )


class BoardAlreadyInUseSquareError(BoardSquareError):
    def __init__(self, board, square):
        super().__init__(square)
        self._availables = list((square1 for square1 in board.empty_squares()))

    def __str__(self):
        return MESSAGES["ALREADY_IN_USE"].format(self._square, str(self._availables))


class BoardInvalidError(Exception):
    def __init__(self, board_str):
        self._board_str = board_str

    def __str__(self):
        return MESSAGES["INVALID_BOARD"].format(
            self._board_str, SQUARES_NUMBER, NO_PLAYER_YET, USER, COMPUTER
        )


class BoardInvalidPlayerError(Exception):
    def __init__(self, player):
        self._player = player

    def __str__(self):
        return MESSAGES["INVALID_PLAYER"].format(
            self._player, NO_PLAYER_YET, USER, COMPUTER
        )
