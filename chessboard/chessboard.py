import numpy
from chessboard.pieces import piece_moves


class Chessboard(object):
  def __init__(self):
    # Define an array containing the names of all of the pieces
    self.piece_names = numpy.full((8, 8), "", dtype='<U20')

    self.possible_moves = numpy.zeros((8, 8), dtype=object)
    for i in range(8):
      for j in range(8):
        self.possible_moves[i, j] = {}

    # Note I use the convention whereby the array printed is in the same layout
    # as the chessboard
    self.piece_names[6, :] = "white pawn"
    self.piece_names[1, :] = "black pawn"
    self.piece_names[7, 0] = "white rook"
    self.piece_names[7, 7] = "white rook"
    self.piece_names[0, 0] = "black rook"
    self.piece_names[0, 7] = "black rook"
    self.piece_names[7, 2] = "white bishop"
    self.piece_names[7, 5] = "white bishop"
    self.piece_names[0, 2] = "black bishop"
    self.piece_names[0, 5] = "black bishop"
    self.piece_names[7, 1] = "white knight"
    self.piece_names[7, 6] = "white knight"
    self.piece_names[0, 1] = "black knight"
    self.piece_names[0, 6] = "black knight"
    self.piece_names[7, 4] = "white king"
    self.piece_names[0, 4] = "black king"
    self.piece_names[7, 3] = "white queen"
    self.piece_names[0, 3] = "black queen"

    self.next_move = "white"
    self.white_king_position = [7, 4]
    self.black_king_position = [0, 4]

    self.find_all_moves()

  def find_all_moves(self):
    for i in range(8):
      for j in range(8):
        # Remove previously stored moves
        self.possible_moves[i, j] = piece_moves(self.piece_names[i, j], [i, j], self.piece_names, self.next_move)

  def move(self, start, finish):
    start = tuple(start)
    finish = tuple(finish)

    # Update piece position
    name = self.piece_names[start]
    self.piece_names[start] = ''
    self.piece_names[finish] = name

    if self.next_move == "white":
      self.next_move = "black"

    else:
      self.next_move = "white"
    
    self.find_all_moves()

    if name == "white king":
      self.white_king_position = list(finish)

    if name == "black king":
      self.black_king_position = list(finish)

    print("Looking for checks:")
    print(self.check_for_check(self.white_king_position, self.piece_names))
    print(self.check_for_check(self.black_king_position, self.piece_names))

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
        if self.piece_names[i, j] == "white pawn":
          piece_array_binary[0, i, j] = 1

        if self.piece_names[i, j] == "white knight":
          piece_array_binary[1, i, j] = 1

        if self.piece_names[i, j] == "white bishop":
          piece_array_binary[2, i, j] = 1

        if self.piece_names[i, j] == "white rook":
          piece_array_binary[3, i, j] = 1

        if self.piece_names[i, j] == "white queen":
          piece_array_binary[4, i, j] = 1

        if self.piece_names[i, j] == "white king":
          piece_array_binary[5, i, j] = 1

        if self.piece_names[i, j] == "black pawn":
          piece_array_binary[6, i, j] = 1

        if self.piece_names[i, j] == "black knight":
          piece_array_binary[7, i, j] = 1

        if self.piece_names[i, j] == "black bishop":
          piece_array_binary[8, i, j] = 1

        if self.piece_names[i, j] == "black rook":
          piece_array_binary[9, i, j] = 1

        if self.piece_names[i, j] == "black queen":
          piece_array_binary[10, i, j] = 1

        if self.piece_names[i, j] == "black king":
          piece_array_binary[11, i, j] = 1

    return piece_array_binary

  def get_positions(self):
    return self.piece_names

  def get_next_move(self):
    return self.next_move

  def check_for_check(self, king_position, piece_names):
    i, j = king_position
    color = piece_names[i, j][0: 5]
    check = False

    if color == "white":
      # Check for knights
      locations = [[i - 1, j - 2], [i + 1, j - 2], [i - 1, j + 2],
                   [i + 1, j + 2], [i - 2, j - 1], [i - 2, j + 1],
                   [i + 2, j - 1], [i + 2, j + 1]]

      for location in locations:
        i_, j_ = location

        if 0 <= i_ and i_ <= 7:
          if 0 <= j_ and j_ <= 7:
            if piece_names[i_, j_] == "black knight":
              check = True

      # Check along the horizontals and verticals (rooks + queens)
      i_, j_ = i, j
      while i_ < 7:
        piece = piece_names[i_ + 1, j_]

        if piece == "black rook" or piece == "black queen":
          check = True
          break

        elif piece == "":
          i_ += 1
          continue

        else:
          break

      i_, j_ = i, j
      while i_ > 0:
        piece = piece_names[i_ - 1, j_]

        if piece == "black rook" or piece == "black queen":
          check = True
          break

        elif piece == "":
          i_ -= 1
          continue

        else:
          break

      i_, j_ = i, j
      while j_ > 0:
        piece = piece_names[i_, j_ - 1]

        if piece == "black rook" or piece == "black queen":
          check = True
          break

        elif piece == "":
          j_ -= 1
          continue

        else:
          break

      i_, j_ = i, j
      while j_ < 7:
        piece = piece_names[i_, j_ + 1]

        if piece == "black rook" or piece == "black queen":
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
        piece = piece_names[i_ + 1, j_ + 1]

        if piece == "black bishop" or piece == "black queen":
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
        piece = piece_names[i_ - 1, j_ + 1]

        if piece == "black bishop" or piece == "black queen":
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
        piece = piece_names[i_ - 1, j_ - 1]

        if piece == "black bishop" or piece == "black queen":
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
        piece = piece_names[i_ + 1, j_ - 1]

        if piece == "black bishop" or piece == "black queen":
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
        if piece_names[i + 1, j - 1] == "black pawn":
          check = True

        if piece_names[i + 1, j + 1] == "black pawn":
          check = True

    if color == "black":
      # Check for knights
      locations = [[i - 1, j - 2], [i + 1, j - 2], [i - 1, j + 2],
                   [i + 1, j + 2], [i - 2, j - 1], [i - 2, j + 1],
                   [i + 2, j - 1], [i + 2, j + 1]]

      for location in locations:
        i_, j_ = location

        if 0 <= i_ and i_ <= 7:
          if 0 <= j_ and j_ <= 7:
            if piece_names[i_, j_] == "white knight":
              check = True

      # Check along the horizontals and verticals (rooks + queens)
      i_, j_ = i, j
      while i_ < 7:
        piece = piece_names[i_ + 1, j_]

        if piece == "white rook" or piece == "white queen":
          check = True
          break

        elif piece == "":
          i_ += 1
          continue

        else:
          break

      i_, j_ = i, j
      while i_ > 0:
        piece = piece_names[i_ - 1, j_]

        if piece == "white rook" or piece == "white queen":
          check = True
          break

        elif piece == "":
          i_ -= 1
          continue

        else:
          break

      i_, j_ = i, j
      while j_ > 0:
        piece = piece_names[i_, j_ - 1]

        if piece == "white rook" or piece == "white queen":
          check = True
          break

        elif piece == "":
          j_ -= 1
          continue

        else:
          break

      i_, j_ = i, j
      while j_ < 7:
        piece = piece_names[i_, j_ + 1]

        if piece == "white rook" or piece == "white queen":
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
        piece = piece_names[i_ + 1, j_ + 1]

        if piece == "white bishop" or piece == "white queen":
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
        piece = piece_names[i_ - 1, j_ + 1]

        if piece == "white bishop" or piece == "white queen":
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
        piece = piece_names[i_ - 1, j_ - 1]

        if piece == "white bishop" or piece == "white queen":
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
        piece = piece_names[i_ + 1, j_ - 1]

        if piece == "white bishop" or piece == "white queen":
          check = True
          break

        elif piece == "":
          i_ += 1
          j_ -= 1
          continue

        else:
          break

      # Check for pawns
      if i > 0:
        if piece_names[i - 1, j - 1] == "white pawn":
          check = True

        if piece_names[i - 1, j + 1] == "white pawn":
          check = True

    return check
