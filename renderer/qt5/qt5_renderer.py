import sys, random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QPainterPath, QPen, QPolygonF
from PyQt5.QtCore import Qt, QRect, QPoint, QPointF

def display(chessboard):
    app = QApplication(sys.argv)
    ex = BoardGuiQt(chessboard)
    sys.exit(app.exec_())


class BoardGuiQt(QWidget):
    bishop_shape = [[0, -0.35], [-0.35, 0], [0, 0.35], [0.35, 0]]
    knight_shape = [[-0.25, 0.35], [0.25, 0.15], [0.25, -0.35], [-0.25, -0.35]]
    king_shape = [[-0.15, -0.4], [-0.15, -0.15], [-0.4, -0.15], [-0.4, 0.15], [-0.15, 0.15], [-0.15, 0.4],
                [0.15, 0.4], [0.15, 0.15], [0.4, 0.15], [0.4, -0.15], [0.15, -0.15], [0.15, -0.4]]
    queen_shape = [[-0.25, -0.35], [-0.4, 0.05], [0, 0.35], [0.4, 0.05], [0.25, -0.35]]
    rook_shape = [[-0.3, -0.3], [-0.3, 0.3], [0.3, 0.3], [0.3, -0.3]]

    def __init__(self, chessboard, square_size=64):
        super().__init__()

        self.selected = None
        self.highlighted = []

        self.rows = 8
        self.columns = 8

        self.light_colour = QColor("#F5F5DC")
        self.dark_colour = QColor("#825A50")
        self.highlight_colour = QColor(3, 252, 202, alpha = 150)
        self.selected_colour = QColor(248, 252, 116, alpha = 200)


        self.chessboard = chessboard
        self.square_size = square_size

        self.board_width = self.columns * square_size
        self.board_height = self.rows * square_size

        self.horizontal_margin = 20
        self.vertical_margin = 30

        self.canvas_width = self.board_width + 2 * self.horizontal_margin
        self.canvas_height = self.board_height + 2 * self.vertical_margin

        self.complicated_shapes = {
            "bishop": self.bishop_shape,
            "knight": self.knight_shape,
            "king": self.king_shape,
            "queen": self.queen_shape,
            "rook": self.rook_shape,
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

    def get_coords(self,e):
        x, y = e.x(), e.y() 
        if x < self.horizontal_margin or x >= self.canvas_width - self.horizontal_margin:
            return
        if y < self.vertical_margin or y >= self.canvas_height - self.vertical_margin:
            return 

        col = int((x - self.horizontal_margin) / self.square_size)
        row = int(8 - ((y - self.vertical_margin) / self.square_size))
        return (col, row)

    def mousePressEvent(self, e):
        coords = self.get_coords(e)
        if not coords:
            return

        if self.selected:
            return
        
        self.selected = coords
        self.update(0,0,self.canvas_width, self.canvas_height)
        

    def mouseReleaseEvent(self, e):
        coords = self.get_coords(e)
        if not coords:
            return
        if self.selected != coords:
            self.selected = None
            self.highlighted = [coords]
        
        self.update(0,0,self.canvas_width, self.canvas_height)



    def draw_square(self, qp, coord, colour):
        qp.setPen(Qt.NoPen)
        qp.fillRect(
            QRect(
                self.horizontal_margin + coord[0] * self.square_size,
                self.vertical_margin + (7- coord[1]) * self.square_size,
                self.square_size,
                self.square_size
            ),
            colour
        )

    def draw_board(self, qp):
        [self.draw_square(qp, (i, j), self.light_colour) for i in range(8) for j in range(8) if (i+j)%2]
        [self.draw_square(qp, (i, j), self.dark_colour) for i in range(8) for j in range(8) if not (i+j)%2]
        label = lambda rect,text: qp.drawText(rect, Qt.AlignCenter, text)

        qp.setPen(Qt.black)
        qp.setFont(QFont('Decorative', 10))
        horizontal_labels = ["A","B","C","D","E","F","G","H"]
        vertical_labels= ["1","2","3","4","5","6","7","8"]
        [label(QRect(self.horizontal_margin + i * self.square_size,self.vertical_margin + self.board_height,self.square_size,self.vertical_margin),horizontal_labels[i]) for i in range(8)]
        [label(QRect(0,self.vertical_margin + i * self.square_size,self.horizontal_margin,self.square_size),vertical_labels[7-i]) for i in range(8)]

    def draw_highlight(self, qp):
        [self.draw_square(qp, coord, self.highlight_colour) for coord in self.highlighted]

    def draw_selected(self, qp):
        if self.selected:
            self.draw_square(qp, self.selected, self.selected_colour)

    def draw_pieces(self, qp):
        for j, rank in enumerate(self.chessboard.piece_names):
            for i, piece in enumerate(rank):
                self.draw_piece(qp, (i,j), piece)
    
    def draw_piece(self, qp, coord, piece):
        i, j = coord
        colour = QColor(piece[0:5])
        outline = QColor("black")
        piece_type = piece[6:]

        qp.setPen(QPen(outline, 5))
        qp.setBrush(colour)

        if piece_type == 'pawn':
            qp.drawEllipse(QPoint(self.horizontal_margin + (i + 0.5) * self.square_size,  self.vertical_margin + (j+0.5) * self.square_size),self.square_size/3, self.square_size/3)
            
        if piece_type in self.complicated_shapes:
            polygon = self.complicated_shapes[piece_type]
            points = [QPointF(self.horizontal_margin + (i + 0.5 +  coord[0]) *self.square_size, self.vertical_margin + (j + 0.5 - coord[1]) * self.square_size) for coord in polygon]
            qp.drawPolygon(QPolygonF(points))

    def move_piece(self, from_pos, to_pos):
        print(f"moved from {from_pos} to {to_pos}")
