def piece_moves(name, position, piece_names):
  i, j = position
  possible_moves = {}

  if name == "white pawn":
    if piece_names[i - 1, j] == "":
      # In this case the pawn is in the position for promotion
      if i == 1:
        possible_moves[(0, j)] = "white queen"
        possible_moves[(0, j)] = "white bishop"
        possible_moves[(0, j)] = "white rook"
        possible_moves[(0, j)] = "white knight"

      # Check if both spaces are available to move
      elif i == 6:
        possible_moves[(i - 1, j)] = "white pawn"
        if piece_names[i - 2, j] == "":
          possible_moves[(i - 2, j)] = "white pawn"

      else:
        possible_moves[(i - 1, j)] = "white pawn"

    # Check if there is a piece diagonally that the pawn can take
    if j > 0:
      if piece_names[i - 1, j - 1] != "":
        possible_moves[(i - 1, j - 1)] = "white pawn"
       
    if j < 7:
      if piece_names[i - 1, j + 1] != "":
        possible_moves[(i - 1, j + 1)] = "white pawn"

  if name == "black pawn":
    if piece_names[i + 1, j] == "":
      # In this case the pawn is in the position for promotion
      if i == 6:
        possible_moves[(7, j)] = "white queen"
        possible_moves[(7, j)] = "white bishop"
        possible_moves[(7, j)] = "white rook"
        possible_moves[(7, j)] = "white knight"

      # Check if both spaces are available to move
      elif i == 1:
        possible_moves[(i + 1, j)] = "white pawn"
        if piece_names[i + 2, j] == "":
          possible_moves[(i + 2, j)] = "white pawn"

      else:
        possible_moves[(i + 1, j)] = "white pawn"

    # Check if there is a piece diagonally that the pawn can take
    if j > 0:
      if piece_names[i + 1, j - 1] != "":
        possible_moves[(i + 1, j - 1)] = "white pawn"
       
    if j < 7:
      if piece_names[i + 1, j + 1] != "":
        possible_moves[(i + 1, j + 1)] = "white pawn"

  return possible_moves
          