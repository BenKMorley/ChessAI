import numpy
import string
from chessboard.pieces import Piece, Colour, piece_moves


class Chessboard():
    """Chessboard class encapsulates all game logic"""

    def __init__(self):
        # Define an array containing the names of all of the pieces
        starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.fen_to_board(starting_fen)

        self.possible_moves = numpy.zeros((8, 8), dtype=object)
        for i in range(8):
            for j in range(8):
                self.possible_moves[i, j] = {}
        self.find_all_moves()

        
    def fen_to_board(self, fen_string):
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

        fen_nums = ["1","2","3","4","5","6","7","8"]
        
        self.board = numpy.full((8, 8), None, dtype=Piece)
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
            self.board[row, col] = fen_translation[char]
            if char == "k":
                self.black_king_position = [row, col]
            if char == "K":
                self.white_king_position = [row, col]
            col += 1

        self.next_move = fen_components[1]
        self.wCastleKing = True if fen_components[2][0] == 'K' else False
        self.wCastleQueen = True if fen_components[2][1] == 'Q' else False
        self.bCastleKing = True if fen_components[2][2] == 'k' else False
        self.bCastleQueen = True if fen_components[2][3] == 'q' else False

        self.en_passant = None if fen_components[3] == '-' else fen_components[3]

        # This is the number of halfmoves since the last capture or pawn advance. The reason for this field is that the value is used in the fifty-move rule
        self.halfmove_clock = int(fen_components[4])

        self.move_number = int(fen_components[5])


    def find_all_moves(self):
        for i in range(8):
            for j in range(8):
                # Remove prior moves
                self.possible_moves[i, j] = {}

                # Find all possible moves ignoring check
                potential_moves = piece_moves(
                    self.board[i, j], [i, j], self.board, self.next_move)
                
                # Now only keep the moves if they don't result in check
                for finish in potential_moves.keys():
                    check = self.check_for_check(self.next_move, [(i, j), finish])

                    if not check:
                        self.possible_moves[i, j][finish] = potential_moves[finish]

    def move(self, start, finish):
        # pdb.set_trace()
        start = tuple(start)
        finish = tuple(finish)

        # Update piece position
        name = self.board[start]
        self.board[start] = ''
        self.board[finish] = name

        if self.next_move == Colour.white:
            self.next_move = "black"

        else:
            self.next_move = "white"

        self.find_all_moves()

        print("Looking for checks:")
        print(self.check_for_check("white"))
        print(self.check_for_check("black"))

    def construct_piece_binary_arrays(self):
        """
          I'm going to use the first index of the binary array to represent the
          type of piece. The key for this is as follows:

          0: white pawn
          1: white knight
          2: white bishop
          3: white rook
          4: white queen
          5: white king
          6: black pawn
          7: black knight
          8: black bishop
          9: black rook
          10: black queen
          11: black king
        """
        piece_array_binary = numpy.zeros((12, 8, 8))

        for i in range(8):
            for j in range(8):
                piece_array_binary[self.board[i, j].value, i, j] = 1

        return piece_array_binary

    def get_positions(self):
        return self.board

    def get_next_move(self):
        return self.next_move

    def check_for_check(self, color, move=None):
        """
            move: expect a list of (2, ) tuples with the start and finish
            positions of the move.
        """
        if move is not None:
            start, finish = move
            # Save the old positions for later restoration
            start_mem = self.board[start]
            finish_mem = self.board[finish]

            # Perform the move (note we are not checking here if the move is
            # valid)
            self.board[finish] = start_mem
            self.board[start] = ''

        i, j = numpy.argwhere(self.board == f"{color} king")[0]
        current_piece = self.board[i, j]
        check = False

        if current_piece.is_white():
            enemyPawn = Piece.bPawn
            enemyKnight = Piece.bKnight
            enemyBishop = Piece.bBishop
            enemyRook = Piece.bRook
            enemyQueen = Piece.bQueen
        else:
            enemyPawn = Piece.wPawn
            enemyKnight = Piece.wKnight
            enemyBishop = Piece.wBishop
            enemyRook = Piece.wRook
            enemyQueen = Piece.wQueen


        # Check for knights
        locations = [[i - 1, j - 2], [i + 1, j - 2], [i - 1, j + 2],
                        [i + 1, j + 2], [i - 2, j - 1], [i - 2, j + 1],
                        [i + 2, j - 1], [i + 2, j + 1]]

        for location in locations:
            i_, j_ = location

            if 0 <= i_ and i_ <= 7:
                if 0 <= j_ and j_ <= 7:
                    if self.board[i_, j_] == Piece.bKnight:
                        check = True

        # Check along the horizontals and verticals (rooks + queens)
        i_, j_ = i, j
        while i_ < 7:
            piece = self.board[i_ + 1, j_]

            if piece == enemyRook or piece == enemyQueen:
                check = True
                break

            elif piece == "":
                i_ += 1
                continue

            else:
                break

        i_, j_ = i, j
        while i_ > 0:
            piece = self.board[i_ - 1, j_]

            if piece == enemyRook or piece == enemyQueen:
                check = True
                break

            elif piece == "":
                i_ -= 1
                continue

            else:
                break

        i_, j_ = i, j
        while j_ > 0:
            piece = self.board[i_, j_ - 1]

            if piece == enemyRook or piece == enemyQueen:
                check = True
                break

            elif piece == "":
                j_ -= 1
                continue

            else:
                break

        i_, j_ = i, j
        while j_ < 7:
            piece = self.board[i_, j_ + 1]

            if piece == enemyRook or piece == enemyQueen:
                check = True
                break

            elif piece == "":
                j_ += 1
                continue

            else:
                break

        # Check along the diagonals for bishops and queens
        i_, j_ = i, j
        while i_ < 7 and j_ < 7:
            piece = self.board[i_ + 1, j_ + 1]

            if piece == enemyBishop or piece == enemyQueen:
                check = True
                break

            elif piece == "":
                i_ += 1
                j_ += 1
                continue

            else:
                break

        i_, j_ = i, j
        while i_ > 0 and j_ < 7:
            piece = self.board[i_ - 1, j_ + 1]

            if piece == enemyBishop or piece == enemyQueen:
                check = True
                break

            elif piece == "":
                i_ -= 1
                j_ += 1
                continue

            else:
                break

        i_, j_ = i, j
        while i_ > 0 and j_ > 0:
            piece = self.board[i_ - 1, j_ - 1]

            if piece == enemyBishop or piece == enemyQueen:
                check = True
                break

            elif piece == "":
                i_ -= 1
                j_ -= 1
                continue

            else:
                break

        i_, j_ = i, j
        while i_ < 7 and j_ > 0:
            piece = self.board[i_ + 1, j_ - 1]

            if piece == enemyBishop or piece == enemyQueen:
                check = True
                break

            elif piece == "":
                i_ += 1
                j_ -= 1
                continue

            else:
                break

        # Check for pawns
        if i < 7:
            if self.board[i + 1, j - 1] == enemyPawn:
                check = True

            if self.board[i + 1, j + 1] == enemyPawn:
                check = True

        if move is not None:
            # Restore pieces to their original positions
            self.board[start] = start_mem
            self.board[finish] = finish_mem
        return check
