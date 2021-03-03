from enum import Enum

class Colour(Enum):
    white = 0
    black = 1

    def opposite(self):
        return Colour((self.value + 1)%2)

class Piece(Enum):
    wPawn = 0
    wKnight = 1
    wBishop = 2
    wRook = 3
    wQueen = 4
    wKing = 5

    bPawn = 6
    bKnight = 7
    bBishop = 8
    bRook = 9
    bQueen = 10
    bKing = 11

    def colour(self):
        return Colour.black if self.value//6 else Colour.white
    
    def is_white(self):
        return self.colour() == Colour.white
    
    def is_black(self):
        return self.colour() == Colour.black

    def is_pawn(self):
        return self.value%6 == 0
    
    def is_knight(self):
        return self.value%6 == 1
    
    def is_bishop(self):
        return self.value%6 == 2

    def is_rook(self):
        return self.value%6 == 3

    def is_queen(self):
        return self.value%6 == 4
    
    def is_king(self):
        return self.value%6 == 5

def white_pawn_moves(position, board):
    possible_moves = {}
    i, j = position

    if board[i - 1, j] is None:
        # In this case the pawn is in the position for promotion
        if i == 1:
            possible_moves[(0, j)] = [Piece.wQueen, Piece.wBishop, Piece.wRook, Piece.wKnight]
        else:
            possible_moves[(i - 1, j)] = [Piece.wPawn]

        # Check if both spaces are available to move
        if i == 6 and board[i - 2, j] is None:
            possible_moves[(i - 2, j)] = [Piece.wPawn]

    # Check if there is a (black) piece diagonally that the pawn can take
    if j > 0:
        possible_enemy = board[i - 1, j - 1]
        if possible_enemy is not None and possible_enemy.is_black():
            possible_moves[(i - 1, j - 1)] = [Piece.wPawn]

    if j < 7:
        possible_enemy = board[i - 1, j + 1]
        if possible_enemy is not None and possible_enemy.is_black():
            possible_moves[(i - 1, j + 1)] = [Piece.wPawn]

    return possible_moves

def black_pawn_moves(position, board):
    possible_moves = {}
    i, j = position

    if board[i + 1, j] is None:
        # In this case the pawn is in the position for promotion
        if i == 6:
            possible_moves[(7, j)] = [Piece.bQueen, Piece.bBishop, Piece.bRook, Piece.bKnight]
        else:
            possible_moves[(i + 1, j)] = [Piece.bPawn]

        # Check if both spaces are available to move
        if i == 1 and board[i + 2, j] is None:
            possible_moves[(i + 2, j)] = [Piece.bPawn]

    # Check if there is a (black) piece diagonally that the pawn can take
    if j > 0:
        possible_enemy = board[i + 1, j - 1]
        if possible_enemy is not None and possible_enemy.is_white():
            possible_moves[(i + 1, j - 1)] = [Piece.bPawn]

    if j < 7:
        possible_enemy = board[i + 1, j + 1]
        if possible_enemy is not None and possible_enemy.is_white():
            possible_moves[(i + 1, j + 1)] = [Piece.bPawn]

    return possible_moves

def knight_moves(position, board):
    moving_piece = board[position]
    possible_moves = {}
    i, j = position

    locations = [[i - 1, j - 2], [i + 1, j - 2], [i - 1, j + 2],
                [i + 1, j + 2], [i - 2, j - 1], [i - 2, j + 1],
                [i + 2, j - 1], [i + 2, j + 1]]

    for location in locations:
        i_, j_ = location
        if i_ >= 0 and i_ <= 7:
            if j_ >= 0 and j_ <= 7:
                possible_enemy = board[i_, j_]
                if possible_enemy is None or possible_enemy.colour() != moving_piece.colour():
                    possible_moves[(i_, j_)] = moving_piece
    
    return possible_moves

def bishop_moves(position, board):
    moving_piece = board[position]
    possible_moves = {}

    # Check top right
    i, j = position
    while i < 7 and j < 7:
        piece = board[i + 1, j + 1]
        if piece is None:
            possible_moves[(i + 1, j + 1)] = moving_piece
            i += 1
            j += 1
            continue

        if piece.colour() != moving_piece.colour():
            possible_moves[(i + 1, j + 1)] = moving_piece
        break

    # Check top left
    i, j = position
    while i < 7 and j > 0:
        piece = board[i + 1, j - 1]
        if piece is None:
            possible_moves[(i + 1, j - 1)] = moving_piece
            i += 1
            j -= 1
            continue

        if piece.colour() != moving_piece.colour():
            possible_moves[(i + 1, j - 1)] = moving_piece
        break

    # Check bottom left
    i, j = position
    while i > 0 and j > 0:
        piece = board[i - 1, j - 1]
        if piece is None:
            possible_moves[(i - 1, j - 1)] = moving_piece
            i -= 1
            j -= 1
            continue

        if piece.colour() != moving_piece.colour():
            possible_moves[(i - 1, j - 1)] = moving_piece
        break

    # Check bottom right
    i, j = position
    while i > 0 and j < 7:
        piece = board[i - 1, j + 1]
        if piece is None:
            possible_moves[(i - 1, j + 1)] = moving_piece
            i -= 1
            j += 1
            continue

        if piece.colour() != moving_piece.colour():
            possible_moves[(i - 1, j + 1)] = moving_piece
        break

    return possible_moves

def rook_moves(position, board):
    moving_piece = board[position]
    possible_moves = {}

    # Check up
    i, j = position
    while i < 7:
        piece = board[i + 1, j]
        if piece is None:
            possible_moves[(i + 1, j)] = moving_piece
            i += 1
            continue

        if piece.colour() != moving_piece.colour():
            possible_moves[(i + 1, j)] = moving_piece
        break


    # Check down
    i, j = position
    while i > 0:
        piece = board[i - 1, j]
        if piece is None:
            possible_moves[(i - 1, j)] = moving_piece
            i -= 1
            continue

        if piece.colour() != moving_piece.colour():
            possible_moves[(i - 1, j)] = moving_piece
        break

    # Check left
    i, j = position
    while j > 0:
        piece = board[i, j - 1]
        if piece is None:
            possible_moves[(i, j - 1)] = moving_piece
            j -= 1
            continue

        if piece.colour() != moving_piece.colour():
            possible_moves[(i, j - 1)] = moving_piece
        break

    # Check right
    i, j = position
    while j < 7:
        piece = board[i, j + 1]
        if piece is None:
            possible_moves[(i, j + 1)] = moving_piece
            j += 1
            continue

        if piece.colour() != moving_piece.colour():
            possible_moves[(i, j + 1)] = moving_piece
        break
    
    return possible_moves

def queen_moves(position, board):
    possible_moves = rook_moves(position, board)
    possible_moves.update(bishop_moves(position, board))
    return possible_moves

def king_moves(position, board):
    moving_piece = board[position]
    possible_moves = {}

    i, j = position
    for i_ in range(max(i - 1, 0), min(i + 1, 7) + 1):
        for j_ in range(max(j - 1, 0), min(j + 1, 7) + 1):
            possible_enemy = board[i_, j_]
            if possible_enemy is None or possible_enemy.colour() != moving_piece.colour():
                possible_moves[(i_, j_)] = moving_piece

    return possible_moves

def piece_moves(position, board):
    piece = board[position]
    if piece is None:
        return None
    if piece == Piece.wPawn:
        return white_pawn_moves(position, board)
    if piece == Piece.bPawn:
        return black_pawn_moves(position, board)
    if piece.is_knight():
        return knight_moves(position, board)
    if piece.is_bishop():
        return bishop_moves(position, board)
    if piece.is_rook():
        return rook_moves(position, board)
    if piece.is_queen():
        return queen_moves(position, board)
    if piece.is_king():
        return king_moves(position, board)

