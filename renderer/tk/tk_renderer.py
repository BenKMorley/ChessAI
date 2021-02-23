import sys
import os
import glob
import tkinter as tk
from PIL import Image, ImageTk

bishop_shape = [[0, -0.35], [-0.35, 0], [0, 0.35], [0.35, 0]]
knight_shape = [[-0.25, 0.35], [0.25, 0.15], [0.25, -0.35], [-0.25, -0.35]]
king_shape = [[-0.15, -0.4], [-0.15, -0.15], [-0.4, -0.15], [-0.4, 0.15], [-0.15, 0.15], [-0.15, 0.4],
            [0.15, 0.4], [0.15, 0.15], [0.4, 0.15], [0.4, -0.15], [0.15, -0.15], [0.15, -0.4]]
queen_shape = [[-0.25, -0.35], [-0.4, 0.05], [0, 0.35], [0.4, 0.05], [0.25, -0.35]]
rook_shape = [[-0.3, -0.3], [-0.3, 0.3], [0.3, 0.3], [0.3, -0.3]]

shape_dict = {'bishop': bishop_shape, 'knight': knight_shape, 'king': king_shape, 'queen': queen_shape, 'rook': rook_shape}

def display(chessboard):
    root = tk.Tk()
    root.title("ChessAI")

    gui = BoardGuiTk(root, chessboard)
    gui.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    gui.draw_pieces()

    root.resizable(0,0)
    root.mainloop()

class BoardGuiTk(tk.Frame):
    pieces = {}
    selected = None
    selected_piece = None
    highlighted = None    
    icons = {}

    rows = 8
    columns = 8

    @property
    def canvas_size(self):
        return (self.columns * self.square_size,
                self.rows * self.square_size)

    def __init__(self, parent, chessboard, square_size=64, colour1="#F5F5DC", colour2="#825A50"):
        self.colour1 = colour1
        self.colour2 = colour2
        self.chessboard = chessboard
        self.square_size = square_size
        self.parent = parent
        self.from_square = None
        self.to_square = None
        self.prompting = False

        canvas_width = self.columns * square_size
        canvas_height = self.rows * square_size

        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.click)

        self.statusbar = tk.Frame(self, height=64)
        self.button_reset = tk.Button(self.statusbar, text="New", fg="black", command=self.draw_pieces)
        self.button_reset.pack(side=tk.LEFT, in_=self.statusbar)

        self.label_status = tk.Label(self.statusbar, text="   White's turn  ", fg="black")
        self.label_status.pack(side=tk.LEFT, expand=0, in_=self.statusbar)

        self.button_quit = tk.Button(self.statusbar, text="Quit", fg="black", command=self.parent.destroy)
        self.button_quit.pack(side=tk.RIGHT, in_=self.statusbar)
        self.statusbar.pack(expand=False, fill="x", side='bottom')


    def draw_square(self, coord):
        col, row = coord
        color = [self.colour2, self.colour1][(row + col) % 2]
        x1 = (col * self.square_size)
        y1 = ((7-row) * self.square_size)
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")

    def draw_piece(self, piece, position):
        col, row = position
        colour = piece[:5]
        piece_type = piece[6:]

        x1 = (col * self.square_size)
        y1 = ((7-row) * self.square_size)
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size

        if piece_type == 'pawn':
            indent = 10
            return self.canvas.create_oval(x1 + indent, y1 + indent, x2 - indent, y2 - indent, fill=colour,outline="black", tags="piece", width=6)

        x1c = ((col + 0.5) * self.square_size)
        y1c = ((7.5-row) * self.square_size)
        size = self.square_size

        if piece_type in shape_dict:
            points = shape_dict[piece_type]
            points = [[point[0] * size + x1c, -point[1] * size + y1c ] for point in points]
            points = [component for point in points for component in point]
            
            return self.canvas.create_polygon(*points, fill=colour,outline="black", tags="piece", width=6)

    def refresh(self, event={}):
        self.canvas.delete("square")
        for row in range(self.rows):
            for col in range(self.columns):
                self.draw_square((row, col))
        
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def click(self, event):
        # Figure out which square we've clicked
        col_size = row_size = event.widget.master.square_size

        current_column = int(event.x / col_size)
        current_row = int(8 - (event.y / row_size))
        print(current_column, current_row)
        self.draw_piece("white_pawn",(current_column, current_row))           

    def draw_pieces(self):
        self.canvas.delete("piece")
        for i in range(8):
            for j in range(8):
                if self.chessboard.get_positions()[i, j] != '':
                    self.draw_piece(self.chessboard.get_positions()[i, j], (j, 7-i))