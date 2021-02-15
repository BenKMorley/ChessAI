import numpy
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.patches import Rectangle, Polygon
from matplotlib.collections import PatchCollection
import pdb
import matplotlib as mpl


class Chessboard(object):
  def __init__(self):
    # Make a chessboard base
    self.board = numpy.ones((8, 8)) - (numpy.indices((8, 8))[0] + numpy.indices((8, 8))[1]) % 2

    self.black_color = numpy.array([130 / 256, 90 / 256, 80 / 256, 1])
    self.white_color = numpy.array([245 / 256, 245 / 256, 220 / 256, 1])

    # Define an array containing the names of all of the pieces
    self.piece_names = numpy.full((8, 8), "", dtype='<U20')

    self.possible_moves = numpy.zeros((8, 8), dtype=object)
    for i in range(8):
      for j in range(8):
        self.possible_moves[i, j] = {}

    # This will be used for clicking on the board
    # self.calibrated_bot_left = False
    # self.bottom_left = 0
    # self.about_to_cal_bot_left = False
    # self.calibrated_top_right = False
    # self.top_right = 0
    # self.about_to_cal_top_right = False

    self.calibrated_bot_left = True
    self.bottom_left = [514, 418]
    self.about_to_cal_bot_left = False
    self.calibrated_top_right = True
    self.top_right = [146, 52]
    self.about_to_cal_top_right = False
    self.to_hide = []

    # Add a piece dictionary
    self.white_pieces = {}
    self.black_pieces = {}

    # 0 indexes white and 1 indexes black
    # Note I use the convention whereby the array printed is in the same layout
    # as the chessboard
    self.white_pieces['pawn'] = numpy.zeros((8, 8))
    self.white_pieces['pawn'][6, :] = numpy.ones(8)
    self.piece_names[6, :] = "white pawn"

    self.black_pieces['pawn'] = numpy.zeros((8, 8))
    self.black_pieces['pawn'][1, :] = numpy.ones(8)
    self.piece_names[1, :] = "black pawn"

    self.white_pieces['rook'] = numpy.zeros((8, 8))
    self.white_pieces['rook'][7, 0] = 1
    self.white_pieces['rook'][7, 7] = 1
    self.piece_names[7, 0] = "white rook"
    self.piece_names[7, 7] = "white rook"

    self.black_pieces['rook'] = numpy.zeros((8, 8))
    self.black_pieces['rook'][0, 0] = 1
    self.black_pieces['rook'][0, 7] = 1
    self.piece_names[0, 0] = "black rook"
    self.piece_names[0, 7] = "black rook"

    self.white_pieces['bishop'] = numpy.zeros((8, 8))
    self.white_pieces['bishop'][7, 2] = 1
    self.white_pieces['bishop'][7, 5] = 1
    self.piece_names[7, 2] = "white bishop"
    self.piece_names[7, 5] = "white bishop"

    self.black_pieces['bishop'] = numpy.zeros((8, 8))
    self.black_pieces['bishop'][0, 2] = 1
    self.black_pieces['bishop'][0, 5] = 1
    self.piece_names[0, 2] = "black bishop"
    self.piece_names[0, 5] = "black bishop"

    self.white_pieces['knight'] = numpy.zeros((8, 8))
    self.white_pieces['knight'][7, 1] = 1
    self.white_pieces['knight'][7, 6] = 1
    self.piece_names[7, 1] = "white knight"
    self.piece_names[7, 6] = "white knight"

    self.black_pieces['knight'] = numpy.zeros((8, 8))
    self.black_pieces['knight'][0, 1] = 1
    self.black_pieces['knight'][0, 6] = 1
    self.piece_names[0, 1] = "black knight"
    self.piece_names[0, 6] = "black knight"
   
    self.white_pieces['king'] = numpy.zeros((8, 8))
    self.white_pieces['king'][7, 4] = 1
    self.piece_names[7, 4] = "white king"

    self.black_pieces['king'] = numpy.zeros((8, 8))
    self.black_pieces['king'][0, 4] = 1
    self.piece_names[0, 4] = "black king"

    self.white_pieces['queen'] = numpy.zeros((8, 8))
    self.white_pieces['queen'][7, 3] = 1
    self.piece_names[7, 3] = "white queen"

    self.black_pieces['queen'] = numpy.zeros((8, 8))
    self.black_pieces['queen'][0, 3] = 1
    self.piece_names[0, 3] = "black queen"

  def find_all_moves(self):
    for i in range(8):
      for j in range(8):
        if self.piece_names[i, j] == "white pawn":
          if self.piece_names[i - 1, j] == "":
            # In this case the pawn is in the position for promotion
            if i == 1:
              self.possible_moves[i][j][(0, j)] = "white queen"
              self.possible_moves[i][j][(0, j)] = "white bishop"
              self.possible_moves[i][j][(0, j)] = "white rook"
              self.possible_moves[i][j][(0, j)] = "white knight"

            else:
              self.possible_moves[i][j][(i - 1, j)] = "white pawn"

  def onclick(self, event):
    print("Click detected")

    bbox_points = numpy.array(self.ax.bbox.get_points())

    bbox_scale = numpy.array(self.ax.bbox._bbox)
    bbox_min = numpy.min(bbox_points, axis=0).reshape(1, 2).repeat(2, axis=0)
    diff = numpy.abs(bbox_points - numpy.roll(bbox_points, 1, axis=0))
    bbox = bbox_min + diff * bbox_scale

    if self.about_to_cal_bot_left:
      self.top_right = [event.x, event.y]
      self.calibrated_bot_left = True
      self.about_to_cal_bot_left = False
      print("Click anywhere")

      return 0

    if self.about_to_cal_top_right:
      self.bottom_left = [event.x, event.y]
      self.calibrated_top_right = True
      self.about_to_cal_top_right = False
      print("Click anywhere")

      return 0

    if not self.calibrated_bot_left:
      print("Please click the bottom-left corner of the board")
      self.about_to_cal_bot_left = True

      return 0
    
    if not self.calibrated_top_right:
      print("Please click the top-right corner of the board")
      self.about_to_cal_top_right = True

      return 0
    
    print(self.top_right)
    print(self.bottom_left)

    # Using the convention for piece[x, y] same as previously
    x = int(numpy.rint(event.y - self.bottom_left[1])) * 8 // int(numpy.rint(self.top_right[1] - self.bottom_left[1]))
    y = int(numpy.rint(event.x - self.bottom_left[0])) * 8 // int(numpy.rint(self.top_right[0] - self.bottom_left[0]))

    print(self.piece_names[x, y])

    # Check for possible moves from this position
    moves = self.possible_moves[x, y]

    # Remove any previous clicks
    for artist in self.to_hide:
      artist.remove()

    self.to_hide = []
    for move in moves.keys():
      if moves[move] == "white pawn":
        self.to_hide.append(self.ax.add_artist(plt.Circle([7 - move[1], 7 - move[0]], radius=0.3, zorder=1, color='r')))

    plt.draw()

  def plot(self, onclick_method):
    viridis = cm.get_cmap('viridis', 2)
    newcolors = viridis(numpy.linspace(0, 1, 2))
    newcolors[0] = self.black_color
    newcolors[1] = self.white_color
    newcmp = ListedColormap(newcolors)

    plt.imshow(self.board, cmap=newcmp, zorder=0)
    ax = plt.gca()
    fig = plt.gcf()

    self.ax = ax
    self.fig = fig

    ax.set_yticklabels(numpy.linspace(0, 8, 9, dtype=int))
    ax.set_xticklabels(numpy.array(['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A', '?'])[::-1])

    indices = numpy.indices((8, 8))

    plt.xlim(-0.5, 7.5)
    plt.ylim(-0.5, 7.5)

    rook_collections = [[], []]
    bishop_collections = [[], []]
    knight_collections = [[], []]
    king_collections = [[], []]
    queen_collections = [[], []]

    # Construct the piece's polygon arrays
    bishop_shape = [[0, -0.35], [-0.35, 0], [0, 0.35], [0.35, 0]]
    knight_shape = [[-0.25, 0.35], [0.25, 0.15], [0.25, -0.35], [-0.25, -0.35]]
    king_shape = [[-0.15, -0.4], [-0.15, -0.15], [-0.4, -0.15], [-0.4, 0.15], [-0.15, 0.15], [-0.15, 0.4],
                  [0.15, 0.4], [0.15, 0.15], [0.4, 0.15], [0.4, -0.15], [0.15, -0.15], [0.15, -0.4]]
    queen_shape = [[-0.25, -0.35], [-0.4, 0.05], [0, 0.35], [0.4, 0.05], [0.25, -0.35]]

    for i in range(8):
      for j in range(8):
        if self.white_pieces['pawn'][i, j] == 1:
          ax.add_artist(plt.Circle([7 - j, 7 - i], radius=0.3, zorder=1, color='w'))
          ax.add_artist(plt.Circle([7 - j, 7 - i], radius=0.3, zorder=1, color='k', fill=False, lw=2))

        if self.black_pieces['pawn'][i, j] == 1:
          ax.add_artist(plt.Circle([7 - j, 7 - i], radius=0.3, zorder=1, color='k'))

        if self.white_pieces['rook'][i, j] == 1:
          rook_collections[0].append(Rectangle(((7 - j) - 0.3, (7 - i) - 0.3), 0.6, 0.6, linewidth=0.3))

        if self.black_pieces['rook'][i, j] == 1:
          rook_collections[1].append(Rectangle(((7 - j) - 0.3, (7 - i) - 0.3), 0.6, 0.6))
        
        if self.white_pieces['bishop'][i, j] == 1:
          bishop_collections[0].append(Polygon(numpy.array([[(7 - j) + k[0], (7 - i) + k[1]] for k in bishop_shape])))

        if self.black_pieces['bishop'][i, j] == 1:
          bishop_collections[1].append(Polygon(numpy.array([[(7 - j) + k[0], (7 - i) + k[1]] for k in bishop_shape])))

        if self.white_pieces['knight'][i, j] == 1:
          knight_collections[0].append(Polygon(numpy.array([[(7 - j) + k[0], (7 - i) + k[1]] for k in knight_shape])))
        
        if self.black_pieces['knight'][i, j] == 1:
          knight_collections[1].append(Polygon(numpy.array([[(7 - j) + k[0], (7 - i) + k[1]] for k in knight_shape])))
        
        if self.white_pieces['king'][i, j] == 1:
          king_collections[0].append(Polygon(numpy.array([[(7 - j) + k[0], (7 - i) + k[1]] for k in king_shape])))
        
        if self.black_pieces['king'][i, j] == 1:
          king_collections[1].append(Polygon(numpy.array([[(7 - j) + k[0], (7 - i) + k[1]] for k in king_shape])))
        
        if self.white_pieces['queen'][i, j] == 1:
          queen_collections[0].append(Polygon(numpy.array([[(7 - j) + k[0], (7 - i) + k[1]] for k in queen_shape])))
        
        if self.black_pieces['queen'][i, j] == 1:
          queen_collections[1].append(Polygon(numpy.array([[(7 - j) + k[0], (7 - i) + k[1]] for k in queen_shape])))

    ax.add_collection(PatchCollection(rook_collections[0], facecolor='w', edgecolor='k', linewidths=2))
    ax.add_collection(PatchCollection(rook_collections[1], facecolor='k'))
    ax.add_collection(PatchCollection(bishop_collections[0], facecolor='w', edgecolor='k', linewidths=2))
    ax.add_collection(PatchCollection(bishop_collections[1], facecolor='k'))
    ax.add_collection(PatchCollection(knight_collections[0], facecolor='w', edgecolor='k', linewidths=2))
    ax.add_collection(PatchCollection(knight_collections[1], facecolor='k'))
    ax.add_collection(PatchCollection(king_collections[0], facecolor='w', edgecolor='k', linewidths=2))
    ax.add_collection(PatchCollection(king_collections[1], facecolor='k'))
    ax.add_collection(PatchCollection(queen_collections[0], facecolor='w', edgecolor='k', linewidths=2))
    ax.add_collection(PatchCollection(queen_collections[1], facecolor='k'))

    x = Rectangle((0, 0), 8, 8, color='r')
    fig = plt.gcf()

    print("Waiting for clicks")
    cid = fig.canvas.mpl_connect('button_press_event', onclick_method)
    print("Got clicks")

    plt.show()

    # [[0.125, 0.10999999999999999], [0.9, 0.88]]


a = Chessboard()
a.find_all_moves()
a.plot(a.onclick)
