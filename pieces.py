import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.patches import Rectangle, Polygon
from matplotlib.collections import PatchCollection
import numpy


bishop_shape = [[0, -0.35], [-0.35, 0], [0, 0.35], [0.35, 0]]
knight_shape = [[-0.25, 0.35], [0.25, 0.15], [0.25, -0.35], [-0.25, -0.35]]
king_shape = [[-0.15, -0.4], [-0.15, -0.15], [-0.4, -0.15], [-0.4, 0.15], [-0.15, 0.15], [-0.15, 0.4],
              [0.15, 0.4], [0.15, 0.15], [0.4, 0.15], [0.4, -0.15], [0.15, -0.15], [0.15, -0.4]]
queen_shape = [[-0.25, -0.35], [-0.4, 0.05], [0, 0.35], [0.4, 0.05], [0.25, -0.35]]


shape_dict = {'bishop': bishop_shape, 'knight': knight_shape, 'king': king_shape, 'queen': queen_shape}


def plot_piece(name, position, ax):
  i, j = position
  color = name[0:5]
  piece_type = name[6:]

  if name == 'possible move':
    return ax.add_artist(plt.Circle([j, 7 - i], radius=0.3, zorder=1, color='r'))

  if piece_type == 'pawn':
    if color == 'white':
      return [ax.add_artist(plt.Circle([j, 7 - i], radius=0.3, zorder=1, color='w')),
              ax.add_artist(plt.Circle([j, 7 - i], radius=0.3, zorder=1, color='k', fill=False, lw=2))]

    if color == 'black':
      return [ax.add_artist(plt.Circle([j, 7 - i], radius=0.3, zorder=1, color='k')),
              ax.add_artist(plt.Circle([j, 7 - i], radius=0.3, zorder=1, color='k', fill=False, lw=2))]

  if piece_type == 'rook':
    if color == 'white':
      return [ax.add_artist(Rectangle(((j) - 0.3, (7 - i) - 0.3), 0.6, 0.6, linewidth=2, facecolor='w', edgecolor='k'))]

    if color == 'black':
      return [ax.add_artist(Rectangle(((j) - 0.3, (7 - i) - 0.3), 0.6, 0.6, linewidth=2, facecolor='k', edgecolor='k'))]

  else:
    shape = shape_dict[piece_type]

    if color == 'white':
      return [ax.add_artist(Polygon(numpy.array([[(j) + k[0], (7 - i) + k[1]] for k in shape]), linewidth=2, facecolor='w', edgecolor='k'))]

    if color == 'black':
      return [ax.add_artist(Polygon(numpy.array([[(j) + k[0], (7 - i) + k[1]] for k in shape]), linewidth=2, facecolor='k', edgecolor='k'))]
