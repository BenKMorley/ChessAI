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

    # Add a piece dictionary
    self.white_pieces = {}
    self.black_pieces = {}

    # 0 indexes white and 1 indexes black
    # Note I use the convention whereby the array printed is in the same layout
    # as the chessboard
    self.white_pieces['white pawn'] = numpy.zeros((8, 8))
    self.white_pieces['white pawn'][6, :] = numpy.ones(8)
    self.piece_names[6, :] = "white pawn"

    self.black_pieces['black pawn'] = numpy.zeros((8, 8))
    self.black_pieces['black pawn'][1, :] = numpy.ones(8)
    self.piece_names[1, :] = "black pawn"

    self.white_pieces['white rook'] = numpy.zeros((8, 8))
    self.white_pieces['white rook'][7, 0] = 1
    self.white_pieces['white rook'][7, 7] = 1
    self.piece_names[7, 0] = "white rook"
    self.piece_names[7, 7] = "white rook"

    self.black_pieces['black rook'] = numpy.zeros((8, 8))
    self.black_pieces['black rook'][0, 0] = 1
    self.black_pieces['black rook'][0, 7] = 1
    self.piece_names[0, 0] = "black rook"
    self.piece_names[0, 7] = "black rook"

    self.white_pieces['white bishop'] = numpy.zeros((8, 8))
    self.white_pieces['white bishop'][7, 2] = 1
    self.white_pieces['white bishop'][7, 5] = 1
    self.piece_names[7, 2] = "white bishop"
    self.piece_names[7, 5] = "white bishop"

    self.black_pieces['black bishop'] = numpy.zeros((8, 8))
    self.black_pieces['black bishop'][0, 2] = 1
    self.black_pieces['black bishop'][0, 5] = 1
    self.piece_names[0, 2] = "black bishop"
    self.piece_names[0, 5] = "black bishop"

    self.white_pieces['white knight'] = numpy.zeros((8, 8))
    self.white_pieces['white knight'][7, 1] = 1
    self.white_pieces['white knight'][7, 6] = 1
    self.piece_names[7, 1] = "white knight"
    self.piece_names[7, 6] = "white knight"

    self.black_pieces['black knight'] = numpy.zeros((8, 8))
    self.black_pieces['black knight'][0, 1] = 1
    self.black_pieces['black knight'][0, 6] = 1
    self.piece_names[0, 1] = "black knight"
    self.piece_names[0, 6] = "black knight"
   
    self.white_pieces['white king'] = numpy.zeros((8, 8))
    self.white_pieces['white king'][7, 4] = 1
    self.piece_names[7, 4] = "white king"

    self.black_pieces['black king'] = numpy.zeros((8, 8))
    self.black_pieces['black king'][0, 4] = 1
    self.piece_names[0, 4] = "black king"

    self.white_pieces['white queen'] = numpy.zeros((8, 8))
    self.white_pieces['white queen'][7, 3] = 1
    self.piece_names[7, 3] = "white queen"

    self.black_pieces['black queen'] = numpy.zeros((8, 8))
    self.black_pieces['black queen'][0, 3] = 1
    self.piece_names[0, 3] = "black queen"

  def find_all_moves(self):
    for i in range(8):
      for j in range(8):
        # Remove previously stored moves
        self.possible_moves[i, j] = piece_moves(self.piece_names[i, j], [i, j], self.piece_names)

  def move(self, start, finish):
    start = tuple(start)
    finish = tuple(finish)
    # pdb.set_trace()

    # Check if a piece has been captured
    color = self.piece_names[start][0:5]

    if self.piece_names[finish] != "":
      if color == "white":
        self.black_pieces[self.piece_names[finish]] = 0
         
      if color == "black":
        self.white_pieces[self.piece_names[finish]] = 0

    # Update piece position
    name = self.piece_names[start]
    self.piece_names[start] = ''
    self.piece_names[finish] = name

    color = name[0:5]
    if color == 'white':
      self.white_pieces[name][start] = 0
      self.white_pieces[name][finish] = 1
    
    else:
      self.black_pieces[name][start] = 0
      self.black_pieces[name][finish] = 1
    
    self.find_all_moves()

  def get_positions(self):
    return self.piece_names
