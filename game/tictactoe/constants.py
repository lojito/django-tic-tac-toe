NO_PLAYER_YET = "0"
USER = "1"
COMPUTER = "2"

RESULT = {
    NO_PLAYER_YET: "The game ended in a tie!",
    USER: "You won the game!",
    COMPUTER: "You lost the game!",
}

SQUARES_NUMBER = 16
SQUARE_NOT_FOUND = -1
WINNING_SQUARES_NUMBER = 4

SQUARES = {
    "ROW_1_COLUMN_1": 0,
    "ROW_1_COLUMN_2": 1,
    "ROW_1_COLUMN_3": 2,
    "ROW_1_COLUMN_4": 3,
    "ROW_2_COLUMN_1": 4,
    "ROW_2_COLUMN_2": 5,
    "ROW_2_COLUMN_3": 6,
    "ROW_2_COLUMN_4": 7,
    "ROW_3_COLUMN_1": 8,
    "ROW_3_COLUMN_2": 9,
    "ROW_3_COLUMN_3": 10,
    "ROW_3_COLUMN_4": 11,
    "ROW_4_COLUMN_1": 12,
    "ROW_4_COLUMN_2": 13,
    "ROW_4_COLUMN_3": 14,
    "ROW_4_COLUMN_4": 15,
}

ROWS_OF_SQUARES = [
    [
        SQUARES["ROW_1_COLUMN_1"],
        SQUARES["ROW_1_COLUMN_2"],
        SQUARES["ROW_1_COLUMN_3"],
        SQUARES["ROW_1_COLUMN_4"],
    ],
    [
        SQUARES["ROW_2_COLUMN_1"],
        SQUARES["ROW_2_COLUMN_2"],
        SQUARES["ROW_2_COLUMN_3"],
        SQUARES["ROW_2_COLUMN_4"],
    ],
    [
        SQUARES["ROW_3_COLUMN_1"],
        SQUARES["ROW_3_COLUMN_2"],
        SQUARES["ROW_3_COLUMN_3"],
        SQUARES["ROW_3_COLUMN_4"],
    ],
    [
        SQUARES["ROW_4_COLUMN_1"],
        SQUARES["ROW_4_COLUMN_2"],
        SQUARES["ROW_4_COLUMN_3"],
        SQUARES["ROW_4_COLUMN_4"],
    ],
    [
        SQUARES["ROW_1_COLUMN_1"],
        SQUARES["ROW_2_COLUMN_1"],
        SQUARES["ROW_3_COLUMN_1"],
        SQUARES["ROW_4_COLUMN_1"],
    ],
    [
        SQUARES["ROW_1_COLUMN_2"],
        SQUARES["ROW_2_COLUMN_2"],
        SQUARES["ROW_3_COLUMN_2"],
        SQUARES["ROW_4_COLUMN_2"],
    ],
    [
        SQUARES["ROW_1_COLUMN_3"],
        SQUARES["ROW_2_COLUMN_3"],
        SQUARES["ROW_3_COLUMN_3"],
        SQUARES["ROW_4_COLUMN_3"],
    ],
    [
        SQUARES["ROW_1_COLUMN_4"],
        SQUARES["ROW_2_COLUMN_4"],
        SQUARES["ROW_3_COLUMN_4"],
        SQUARES["ROW_4_COLUMN_4"],
    ],
    [
        SQUARES["ROW_1_COLUMN_1"],
        SQUARES["ROW_2_COLUMN_2"],
        SQUARES["ROW_3_COLUMN_3"],
        SQUARES["ROW_4_COLUMN_4"],
    ],
    [
        SQUARES["ROW_1_COLUMN_4"],
        SQUARES["ROW_2_COLUMN_3"],
        SQUARES["ROW_3_COLUMN_2"],
        SQUARES["ROW_4_COLUMN_1"],
    ],
]

MESSAGES = {
    "INVALID_POSITION": "The position {} is invalid. Positions range from 0 to {}.",
    "ALREADY_IN_USE": "The position {} is already in use. The positions available are : {}.",
    "INVALID_BOARD": "The Tic-Tac-Toe board {} is invalid. \
Expecting a string of {} characters composed of '{}' indicating that nor user, \
nor the computer has played on a square, '{}' representing the user who is playing \
against the computer and '{}' for the computer itself as the only possible values.",
    "INVALID_PLAYER": "Invalid player {}. Valids values for a player are '{}' \
indicating that nor user, nor the computer has played on a square, \
'{}' representing the user who is playing against the computer and '{}' for the computer itself.",
    "BOARD_IS_FULL": "The board has no empty square to play on.",
}
