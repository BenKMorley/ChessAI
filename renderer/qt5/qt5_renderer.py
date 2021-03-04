import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QPainterPath, QPen, QPolygonF
from PyQt5.QtCore import Qt, QRect, QPoint, QPointF
from chessboard.pieces.pieces import Piece


def display(chessboard):
    app = QApplication(sys.argv)
    ex = BoardGuiQt(chessboard)
    sys.exit(app.exec_())


class BoardGuiQt(QWidget):
    bishop_shape = [[0, -0.35], [-0.35, 0], [0, 0.35], [0.35, 0]]
    knight_shape = [[-0.25, 0.35], [0.25, 0.15], [0.25, -0.35], [-0.25, -0.35]]
    king_shape = [[-0.15, -0.4], [-0.15, -0.15], [-0.4, -0.15], [-0.4, 0.15], [-0.15, 0.15], [-0.15, 0.4],
                  [0.15, 0.4], [0.15, 0.15], [0.4, 0.15], [0.4, -0.15], [0.15, -0.15], [0.15, -0.4]]
    queen_shape = [[-0.25, -0.35], [-0.4, 0.05],
                   [0, 0.35], [0.4, 0.05], [0.25, -0.35]]
    rook_shape = [[-0.3, -0.3], [-0.3, 0.3], [0.3, 0.3], [0.3, -0.3]]

    def __init__(self, chessboard, square_size=64):
        super().__init__()

        self.selected = None
        self.highlighted = []

        self.rows = 8
        self.columns = 8

        self.light_colour = QColor("#F5F5DC")
        self.dark_colour = QColor("#825A50")
        self.highlight_colour = QColor(3, 252, 202, alpha=150)
        self.selected_colour = QColor(248, 252, 116, alpha=200)

        self.chessboard = chessboard
        self.square_size = square_size

        self.board_width = self.columns * square_size
        self.board_height = self.rows * square_size

        self.horizontal_margin = 20
        self.vertical_margin = 30

        self.canvas_width = self.board_width + 2 * self.horizontal_margin
        self.canvas_height = self.board_height + 2 * self.vertical_margin

        self.complicated_shapes = {
            Piece.wBishop : self.bishop_shape,
            Piece.bBishop : self.bishop_shape,
            Piece.wKnight: self.knight_shape,
            Piece.bKnight: self.knight_shape,
            Piece.wKing: self.king_shape,
            Piece.bKing: self.king_shape,
            Piece.wQueen: self.queen_shape,
            Piece.bQueen: self.queen_shape,
            Piece.wRook: self.rook_shape,
            Piece.bRook: self.rook_shape,
        }

        self.holding = None

        self.init_UI()

    def init_UI(self):

        self.setGeometry(0, 0, self.canvas_width, self.canvas_height)
        self.setWindowTitle('ChessAI')
        self.setWindowIcon(QIcon('res/knight.png'))

        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.draw_board(qp)
        self.draw_highlight(qp)
        self.draw_selected(qp)
        self.draw_pieces(qp)
        qp.end()

    def get_coords(self, e):
        x, y = e.x(), e.y()
        if x < self.horizontal_margin or x >= self.canvas_width - self.horizontal_margin:
            return
        if y < self.vertical_margin or y >= self.canvas_height - self.vertical_margin:
            return

        col = int((x - self.horizontal_margin) / self.square_size)
        row = int(8 - ((y - self.vertical_margin) / self.square_size))
        return (col, row)

    def to_weird_coords(self, coords):
        return (7-coords[1], coords[0])

    def from_weird_coords(self, coords):
        return (coords[1], 7-coords[0])

    def piece_at(self, coords):
        c = self.to_weird_coords(coords)
        return self.chessboard.get_positions()[c[0], c[1]]

    def posible_moves(self, coords):
        c = self.to_weird_coords(coords)
        moves = self.chessboard.possible_moves[c[0], c[1]].keys()
        return [self.from_weird_coords(move) for move in moves]

    def move(self, from_coord, to_coord):
        self.chessboard.move(self.to_weird_coords(
            from_coord), self.to_weird_coords(to_coord))

    def mousePressEvent(self, e):
        coords = self.get_coords(e)
        if not coords:
            return

        if coords in self.highlighted:
            return

        piece = self.piece_at(coords)
        if piece != "":
            self.selected = coords
            self.highlighted = self.posible_moves(self.selected)
            self.update(0, 0, self.canvas_width, self.canvas_height)

    def mouseReleaseEvent(self, e):
        coords = self.get_coords(e)
        if not coords:
            return

        if self.selected and self.selected != coords:
            if coords in self.highlighted:
                self.move(self.selected, coords)
                self.selected = None
                self.highlighted = []
                self.update(0, 0, self.canvas_width, self.canvas_height)
            else:
                piece = self.piece_at(coords)
                if piece != "":
                    self.selected = coords
                    self.highlighted = self.posible_moves(self.selected)
                    self.update(0, 0, self.canvas_width, self.canvas_height)

    def draw_square(self, qp, coord, colour):
        qp.setPen(Qt.NoPen)
        qp.fillRect(
            QRect(
                self.horizontal_margin + coord[0] * self.square_size,
                self.vertical_margin + (7 - coord[1]) * self.square_size,
                self.square_size,
                self.square_size
            ),
            colour
        )

    def draw_board(self, qp):
        [self.draw_square(qp, (i, j), self.light_colour)
         for i in range(8) for j in range(8) if (i+j) % 2]
        [self.draw_square(qp, (i, j), self.dark_colour)
         for i in range(8) for j in range(8) if not (i+j) % 2]

        def label(rect, text): return qp.drawText(rect, Qt.AlignCenter, text)

        qp.setPen(Qt.black)
        qp.setFont(QFont('Decorative', 10))
        horizontal_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
        vertical_labels = ["1", "2", "3", "4", "5", "6", "7", "8"]
        [label(QRect(self.horizontal_margin + i * self.square_size, self.vertical_margin + self.board_height,
                     self.square_size, self.vertical_margin), horizontal_labels[i]) for i in range(8)]
        [label(QRect(0, self.vertical_margin + i * self.square_size, self.horizontal_margin,
                     self.square_size), vertical_labels[7-i]) for i in range(8)]

    def draw_highlight(self, qp):
        [self.draw_square(qp, coord, self.highlight_colour)
         for coord in self.highlighted]

    def draw_selected(self, qp):
        if self.selected:
            self.draw_square(qp, self.selected, self.selected_colour)

    def draw_pieces(self, qp):
        for j, rank in enumerate(self.chessboard.get_positions()):
            for i, piece in enumerate(rank):
                if piece is not None:
                    self.draw_piece(qp, (i, j), piece)

    def draw_piece(self, qp, coord, piece):
        i, j = coord
        colour = QColor("white" if piece.is_white() else "black")
        outline = QColor("black")

        qp.setPen(QPen(outline, 5))
        qp.setBrush(colour)

        if piece.is_pawn():
            qp.drawEllipse(QPoint(self.horizontal_margin + (i + 0.5) * self.square_size,
                                  self.vertical_margin + (j+0.5) * self.square_size), self.square_size/3, self.square_size/3)

        if piece.is_enpassant():
            qp.drawEllipse(QPoint(self.horizontal_margin + (i + 0.5) * self.square_size,
                                  self.vertical_margin + (j+0.5) * self.square_size), self.square_size/4, self.square_size/4)

        if piece in self.complicated_shapes:
            polygon = self.complicated_shapes[piece]
            points = [QPointF(self.horizontal_margin + (i + 0.5 + coord[0]) * self.square_size,
                              self.vertical_margin + (j + 0.5 - coord[1]) * self.square_size) for coord in polygon]
            qp.drawPolygon(QPolygonF(points))

    def move_piece(self, from_pos, to_pos):
        print(f"moved from {from_pos} to {to_pos}")
