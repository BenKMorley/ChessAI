import numpy
from chessboard.pieces.pieces import Piece, Colour, piece_moves
from enum import Enum
from copy import copy


class GameState(Enum):
    ongoing = 0
    w_win = 1
    b_win = 2
    draw = 3

    def is_gg(self):
        if self.value > 0:
            return True


class Move(object):
    def __init__(self, start, finish, end_piece):
        self.start = start
        self.finish = finish
        self.end_piece = end_piece
        self.letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

    def __repr__(self):
        i, j = self.start
        i2, j2 = self.finish

        print(f"{self.board[self.start]} from ", end='')
        print(f"{self.letters[j]}{8 - i} to ", end='')
        print(f"{self.letters[j2]}{8 - i2} becoming ", end='')
        print(f"{self.end_piece}")

    def __str__(self):
        i, j = self.start
        i2, j2 = self.finish

        return f"{self.board[self.start]} from " + \
               f"{self.letters[j]}{8 - i} to " +\
               f"{self.letters[j2]}{8 - i2} becoming " +\
               f"{self.end_piece}"


class Chessboard():
    """Chessboard class encapsulates all game logic"""
    def __init__(self):
        # Define an array containing the names of all of the pieces
        self.board = numpy.full((8, 8), None, dtype=Piece)
        self.game_state = GameState.ongoing
        self.next_move = Colour.white
        self.w_castle_king = True
        self.w_castle_queen = True
        self.b_castle_king = True
        self.b_castle_queen = True

        self.en_passant = 0
        self.halfmove_clock = 0
        self.move_number = 0

        # TO DO: Reconstruct code using self.moves_list instead
        self.possible_moves = numpy.zeros((8, 8), dtype=object)
        for i in range(8):
            for j in range(8):
                self.possible_moves[i, j] = {}

        self.moves_list = []

    def start(self):
        self.find_all_moves()
        self.find_all_binary_arrays()

    def find_all_moves(self):
        total = 0
        self.moves_list = []

        for i in range(8):
            for j in range(8):
                # Remove prior moves
                self.possible_moves[i, j] = {}

                current_piece = self.board[i, j]

                # Skip of this isn't a piece or it has wrong colour
                if current_piece is None or current_piece.colour() != self.next_move:
                    continue

                # Find all possible moves ignoring check
                potential_moves = piece_moves((i, j), self.board)

                # Now only keep the moves if they don't result in check
                for finish in potential_moves.keys():
                    check = self.check_for_check(self.next_move, [(i, j), finish])

                    if not check:
                        self.possible_moves[i, j][finish] = potential_moves[finish]
                        total += 1

                        for final_piece in potential_moves[finish]:
                            self.moves_list.append(Move((i, j), finish, final_piece))

        return total

    def move(self, start, finish):
        # Clear out any old en passant pieces
        for i in range(8):
            for j in range(8):
                if self.board[i, j] == Piece.wPawnEn:
                    if finish == (i + 1, j) and self.possible_moves[start][finish][0] == Piece.bPawn:
                        self.board[i, j] = None
                    else:
                        self.board[i, j] = Piece.wPawn

                if self.board[i, j] == Piece.bPawnEn:
                    if finish == (i - 1, j) and self.possible_moves[start][finish][0] == Piece.wPawn:
                        self.board[i, j] = None
                    else:
                        self.board[i, j] = Piece.bPawn

        start = tuple(start)
        finish = tuple(finish)

        # Update piece position
        piece = self.board[start]
        self.board[start] = None

        if len(self.possible_moves[start][finish]) == 1:
            self.board[finish] = self.possible_moves[start][finish][0]

        else:
            print("TODO: GUI to select piece for pawn promotion")

        if self.next_move == Colour.white:
            self.move_number += 1

        self.next_move = self.next_move.opposite()

        # Find possible moves for the next player
        total_moves = self.find_all_moves()
        print("")
        print(total_moves)

        # If there are no possible moves the game ends
        if total_moves == 0:
            check = self.check_for_check(self.next_move)

            # Stalemate
            if not check:
                self.game_state = GameState.draw

            else:
                if self.next_move == Colour.white:
                    self.game_state = GameState.b_win

                else:
                    self.game_state = GameState.w_win

        # print(self.game_state)

        return self.game_state

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
          6: white pawn en-passant
          7: black pawn
          8: black knight
          9: black bishop
          10: black rook
          11: black queen
          12: black king
          13: black pawn en-passant
        """
        piece_array_binary = numpy.zeros((14, 8, 8))

        for i in range(8):
            for j in range(8):
                if self.board[i, j] is not None:
                    piece_array_binary[self.board[i, j].value, i, j] = 1

        return piece_array_binary

    def generate_potential_board_arrays(self):
        total_moves = self.find_all_moves()

        base = self.construct_piece_binary_arrays()

        board_options = []
        count = 0

        for i in range(8):
            for j in range(8):
                for key in self.possible_moves[i, j]:
                    finish_x, finish_y = key
                    for piece in self.possible_moves[key]:
                        start = copy(base)

                        # Remove the piece at start
                        start[self.board[i, j].value, i, j] = 0

                        # Add the piece at the end
                        start[piece.value, i, j] = 1

    def get_positions(self):
        return self.board

    def get_board_state(self):
        return self.next_move

    def at_position(self, position):
        i, j = position
        if 0 <= i and i <= 7:
            if 0 <= j and j <= 7:
                return self.board[i, j]

        return None

    def check_for_check(self, colour, move=None):
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
            self.board[start] = None

        king = Piece.wKing if colour == Colour.white else Piece.bKing
        i, j = numpy.argwhere(self.board == king)[0]

        if colour == Colour.white:
            enemy_pawn = Piece.bPawn
            enemy_knight = Piece.bKnight
            enemy_bishop = Piece.bBishop
            enemy_rook = Piece.bRook
            enemy_queen = Piece.bQueen
        else:
            enemy_pawn = Piece.wPawn
            enemy_knight = Piece.wKnight
            enemy_bishop = Piece.wBishop
            enemy_rook = Piece.wRook
            enemy_queen = Piece.wQueen

        check = self.check_pawn_positions((i, j), colour, [enemy_pawn]) or \
         self.check_knight_positions((i, j), [enemy_knight]) or \
         self.check_straights((i, j), [enemy_rook, enemy_queen]) or \
         self.check_diagonals((i, j), [enemy_bishop, enemy_queen])

        if move is not None:
            # Restore pieces to their original positions
            self.board[start] = start_mem
            self.board[finish] = finish_mem
        return check

    def check_pawn_positions(self, position, colour, enemies):
        # Check for pawns
        i, j = position
        if colour == Colour.white:
            pawn_locations = [[i - 1, j + 1], [i - 1, j - 1]]

        else:
            pawn_locations = [[i + 1, j + 1], [i + 1, j - 1]]

        for location in pawn_locations:
            if self.at_position(location) in enemies:
                return True

        return False

    def check_knight_positions(self, position, enemies):
        i, j = position
        knight_positions = [[i - 1, j - 2], [i + 1, j - 2], [i - 1, j + 2],
                            [i + 1, j + 2], [i - 2, j - 1], [i - 2, j + 1],
                            [i + 2, j - 1], [i + 2, j + 1]]

        for pos in knight_positions:
            if self.at_position(pos) in enemies:
                return True

        return False

    def check_diagonals(self, position, enemies):
        # Check along the diagonals for bishops and queens
        i, j = position
        while i < 7 and j < 7:
            piece = self.board[i + 1, j + 1]
            if piece in enemies:
                return True
            elif piece is not None:
                break
            i += 1
            j += 1

        i, j = position
        while i > 0 and j < 7:
            piece = self.board[i - 1, j + 1]
            if piece in enemies:
                return True
            elif piece is not None:
                break
            i -= 1
            j += 1

        i, j = position
        while i > 0 and j > 0:
            piece = self.board[i - 1, j - 1]
            if piece in enemies:
                return True
            elif piece is not None:
                break
            i -= 1
            j -= 1

        i, j = position
        while i < 7 and j > 0:
            piece = self.board[i + 1, j - 1]
            if piece in enemies:
                return True
            elif piece is not None:
                break
            i += 1
            j -= 1

        return False

    def check_straights(self, position, enemies):
        # Check along the horizontals and verticals (rooks + queens)
        i, j = position
        while i < 7:
            piece = self.board[i + 1, j]
            if piece in enemies:
                return True
            elif piece is not None:
                break
            i += 1

        i, j = position
        while i > 0:
            piece = self.board[i - 1, j]
            if piece in enemies:
                return True
            elif piece is not None:
                break
            i -= 1

        i, j = position
        while j > 0:
            piece = self.board[i, j - 1]
            if piece in enemies:
                return True
            elif piece is not None:
                break
            j -= 1

        i, j = position
        while j < 7:
            piece = self.board[i, j + 1]
            if piece in enemies:
                return True
            elif piece is not None:
                break
            j += 1

        return False

    def find_all_binary_arrays(self):
        binary_arrays = []

        for move in self.moves_list:
            # Save the old positions for later restoration
            start_mem = self.board[move.start]
            finish_mem = self.board[move.finish]

            # Perform the move (note we are not checking here if the move is
            # valid)
            self.board[move.finish] = move.end_piece
            self.board[move.start] = None

            binary_arrays.append(self.construct_piece_binary_arrays())

            # Restore pieces to their original positions
            self.board[move.start] = start_mem
            self.board[move.finish] = finish_mem

        return binary_arrays
