import numpy
from chessboard.pieces.pieces import Piece, Colour
from chessboard.chessboard import Chessboard

def fen_to_chessboard(game, fen_string):
    fen_components = fen_string.split()
    if len(fen_components) != 6:
        print("error loading fen_string: too many components")
        return

    fen_translation = {
        "P": Piece.wPawn,
        "N": Piece.wKnight,
        "B": Piece.wBishop,
        "R": Piece.wRook,
        "Q": Piece.wQueen,
        "K": Piece.wKing,

        "p": Piece.bPawn,
        "n": Piece.bKnight,
        "b": Piece.bBishop,
        "r": Piece.bRook,
        "q": Piece.bQueen,
        "k": Piece.bKing,
    }

    fen_nums = ["1", "2", "3", "4", "5", "6", "7", "8"]

    row = 0
    col = 0
    for char in fen_components[0]:
        if char == "/":
            row += 1
            col = 0
            continue
        if char in fen_nums:
            col += int(char)
            continue
        game.board[row, col] = fen_translation[char]
        col += 1

    game.next_move = Colour.white if fen_components[1] == 'w' else Colour.black
    game.w_castle_king = True if fen_components[2][0] == 'K' else False
    game.w_castle_queen = True if fen_components[2][1] == 'Q' else False
    game.b_castle_king = True if fen_components[2][2] == 'k' else False
    game.b_castle_queen = True if fen_components[2][3] == 'q' else False

    game.en_passant = None if fen_components[3] == '-' else fen_components[3]

    # This is the number of halfmoves since the last capture or pawn advance. The reason for this field is that the value is used in the fifty-move rule
    game.halfmove_clock = int(fen_components[4])

    game.move_number = int(fen_components[5])
    game.find_all_moves()
    return game