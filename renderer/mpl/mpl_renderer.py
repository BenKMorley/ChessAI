import numpy
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.patches import Rectangle, Polygon
from matplotlib.collections import PatchCollection
import pdb
import matplotlib as mpl


bishop_shape = [[0, -0.35], [-0.35, 0], [0, 0.35], [0.35, 0]]
knight_shape = [[-0.25, 0.35], [0.25, 0.15], [0.25, -0.35], [-0.25, -0.35]]
king_shape = [[-0.15, -0.4], [-0.15, -0.15], [-0.4, -0.15], [-0.4, 0.15], [-0.15, 0.15], [-0.15, 0.4],
              [0.15, 0.4], [0.15, 0.15], [0.4, 0.15], [0.4, -0.15], [0.15, -0.15], [0.15, -0.4]]
queen_shape = [[-0.25, -0.35], [-0.4, 0.05], [0, 0.35], [0.4, 0.05], [0.25, -0.35]]


shape_dict = {'bishop': bishop_shape, 'knight': knight_shape, 'king': king_shape, 'queen': queen_shape}

def display(chessboard):
    renderer = BoardGuiMatplotlib(chessboard)
    chessboard.find_all_moves()
    renderer.plot()


class BoardGuiMatplotlib():
    def __init__(self, chessboard):
        self.chessboard = chessboard

        # Make a chessboard base
        self.board = (numpy.ones((8, 8)) - (numpy.indices((8, 8))[0] + numpy.indices((8, 8))[1]) + 1) % 2

        self.black_color = numpy.array([130 / 256, 90 / 256, 80 / 256, 1])
        self.white_color = numpy.array([245 / 256, 245 / 256, 220 / 256, 1])

        # For keeping track of the artists on the plot
        self.artists_current = []
        self.artists_new = []

        # This will be used for clicking on the board
        # self.calibrated_bot_left = False
        # self .bottom_left = 0
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
        self.select_moves = {}

    def plot(self):
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

        self.plot_pieces()

        fig = plt.gcf()

        print("Waiting for clicks")
        cid = fig.canvas.mpl_connect('button_press_event', self.onclick)
        print("Got clicks")

        self.refresh_artists()
        plt.show()

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
        y = 7 - int(numpy.rint(event.x - self.bottom_left[0])) * 8 // int(numpy.rint(self.top_right[0] - self.bottom_left[0]))

        print(self.chessboard.piece_names[x, y])

        # pdb.set_trace()

        # Check for possible moves from this position
        moves = self.chessboard.possible_moves[x, y]
        flag = False

        # Check if someone has selected a selected move
        if (x, y) in self.select_moves:
            origin = self.select_moves[(x, y)]
            self.chessboard.move(origin, (x, y))
            flag = True
        
        self.plot_pieces()

        # Remove any previous clicks
        for movement in list(self.select_moves.keys()):
            del self.select_moves[movement]

        if not flag:
            self.select_moves = {}
            for move in moves.keys():
                self.artists_new.append(self.plot_possible_move([move[0], move[1]]))
                self.select_moves[(move[0], move[1])] = (x, y)
            print(self.select_moves)

        # pdb.set_trace()
        self.refresh_artists()
        plt.draw()

    def plot_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.chessboard.piece_names[i, j] != '':
                    self.artists_new.extend(self.plot_piece(self.chessboard.piece_names[i, j], [i, j]))
    
    def refresh_artists(self):
        for artist in self.artists_current:
            artist.remove()
        self.artists_current = self.artists_new
        self.artists_new = []
        

    def plot_possible_move(self, position):
        i, j = position
        return self.ax.add_artist(plt.Circle([j, 7 - i], radius=0.3, zorder=1, color='r'))

    def plot_piece(self, name, position):
        i, j = position
        color = name[0:5]
        piece_type = name[6:]

        if piece_type == 'pawn':
            if color == 'white':
                return [self.ax.add_artist(plt.Circle([j, 7 - i], radius=0.3, zorder=1, color='w')),
                    self.ax.add_artist(plt.Circle([j, 7 - i], radius=0.3, zorder=1, color='k', fill=False, lw=2))]

            if color == 'black':
                return [self.ax.add_artist(plt.Circle([j, 7 - i], radius=0.3, zorder=1, color='k')),
                    self.ax.add_artist(plt.Circle([j, 7 - i], radius=0.3, zorder=1, color='k', fill=False, lw=2))]

        if piece_type == 'rook':
            if color == 'white':
                return [self.ax.add_artist(Rectangle(((j) - 0.3, (7 - i) - 0.3), 0.6, 0.6, linewidth=2, facecolor='w', edgecolor='k'))]

            if color == 'black':
                return [self.ax.add_artist(Rectangle(((j) - 0.3, (7 - i) - 0.3), 0.6, 0.6, linewidth=2, facecolor='k', edgecolor='k'))]

        else:
            shape = shape_dict[piece_type]

            if color == 'white':
                return [self.ax.add_artist(Polygon(numpy.array([[(j) + k[0], (7 - i) + k[1]] for k in shape]), linewidth=2, facecolor='w', edgecolor='k'))]

            if color == 'black':
                return [self.ax.add_artist(Polygon(numpy.array([[(j) + k[0], (7 - i) + k[1]] for k in shape]), linewidth=2, facecolor='k', edgecolor='k'))]
