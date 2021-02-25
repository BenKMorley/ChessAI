def piece_moves(name, position, piece_names, next_move):
  i, j = position
  possible_moves = {}

  color = name[0: 5]

  if color == next_move:
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

      # Check if there is a (black) piece diagonally that the pawn can take
      if j > 0:
        if piece_names[i - 1, j - 1][0: 5] == "black":
          possible_moves[(i - 1, j - 1)] = "white pawn"
         
      if j < 7:
        if piece_names[i - 1, j - 1][0: 5] == "black":
          possible_moves[(i - 1, j + 1)] = "white pawn"

    if name == "white rook":
      # Check up
      record_i = i
      record_j = j

      while i < 7:
        if piece_names[i + 1, j][0: 5] == "":
          possible_moves[(i + 1, j)] = "white rook"

        if piece_names[i + 1, j][0: 5] == "black":
          possible_moves[(i + 1, j)] = "white rook"
          break

        if piece_names[i + 1, j][0: 5] == "white":
          break

        i += 1

      i = record_i
      # Check down
      while i > 0:
        if piece_names[i - 1, j][0: 5] == "":
          possible_moves[(i - 1, j)] = "white rook"

        if piece_names[i - 1, j][0: 5] == "black":
          possible_moves[(i - 1, j)] = "white rook"
          break

        if piece_names[i - 1, j][0: 5] == "white":
          break

        i -= 1

      i = record_i
      # Check left
      while j > 0:
        if piece_names[i, j - 1][0: 5] == "":
          possible_moves[(i, j - 1)] = "white rook"

        if piece_names[i, j - 1][0: 5] == "black":
          possible_moves[(i, j - 1)] = "white rook"
          break

        if piece_names[i, j - 1][0: 5] == "white":
          break

        j -= 1

      j = record_j
      # Check right
      while j < 7:
        if piece_names[i, j + 1][0: 5] == "":
          possible_moves[(i, j + 1)] = "white rook"

        if piece_names[i, j + 1][0: 5] == "black":
          possible_moves[(i, j + 1)] = "white rook"
          break

        if piece_names[i, j + 1][0: 5] == "white":
          break

        j += 1

    if name == "white bishop":
      # Check up
      record_i = i
      record_j = j

      while i < 7 and j < 7:
        if piece_names[i + 1, j + 1][0: 5] == "":
          possible_moves[(i + 1, j + 1)] = "white bishop"

        if piece_names[i + 1, j + 1][0: 5] == "black":
          possible_moves[(i + 1, j + 1)] = "white bishop"
          break

        if piece_names[i + 1, j + 1][0: 5] == "white":
          break

        i += 1
        j += 1

      i = record_i
      j = record_j

      while i < 7 and j > 0:
        if piece_names[i + 1, j - 1][0: 5] == "":
          possible_moves[(i + 1, j - 1)] = "white bishop"

        if piece_names[i + 1, j - 1][0: 5] == "black":
          possible_moves[(i + 1, j - 1)] = "white bishop"
          break

        if piece_names[i + 1, j - 1][0: 5] == "white":
          break

        i += 1
        j -= 1

      i = record_i
      j = record_j

      while i > 0 and j > 0:
        if piece_names[i - 1, j - 1][0: 5] == "":
          possible_moves[(i - 1, j - 1)] = "white bishop"

        if piece_names[i - 1, j - 1][0: 5] == "black":
          possible_moves[(i - 1, j - 1)] = "white bishop"
          break

        if piece_names[i - 1, j - 1][0: 5] == "white":
          break

        i -= 1
        j -= 1

      i = record_i
      j = record_j

      while i > 0 and j < 7:
        if piece_names[i - 1, j + 1][0: 5] == "":
          possible_moves[(i - 1, j + 1)] = "white bishop"

        if piece_names[i - 1, j + 1][0: 5] == "black":
          possible_moves[(i - 1, j + 1)] = "white bishop"
          break

        if piece_names[i - 1, j + 1][0: 5] == "white":
          break

        i -= 1
        j += 1

      i = record_i
      j = record_j

    if name == "white queen":
      possible_moves = piece_moves("white rook", position, piece_names,
                                   next_move)
      possible_moves2 = piece_moves("white bishop", position, piece_names,
                                    next_move)

      possible_moves.update(possible_moves2)

    if name == "white king":
      for i_ in range(max(i - 1, 0), min(i + 1, 7) + 1):
        for j_ in range(max(j - 1, 0), min(j + 1, 7) + 1):
          if piece_names[i_, j_][0: 5] != "white":
            possible_moves[(i_, j_)] = "white king"

    if name == "white knight":
      locations = [[i - 1, j - 2], [i + 1, j - 2], [i - 1, j + 2],
                   [i + 1, j + 2], [i - 2, j - 1], [i - 2, j + 1],
                   [i + 2, j - 1], [i + 2, j + 1]]

      for location in locations:
        i_, j_ = location[0], location[1]
        if (i_ >= 0) and (i_ <= 7):
          if (j_ >= 0) and (j_ <= 7):
            if piece_names[i_, j_][0: 5] != "white":
              possible_moves[(i_, j_)] = "white knight"

    if name == "black pawn":
      if piece_names[i + 1, j] == "":
        # In this case the pawn is in the position for promotion
        if i == 6:
          possible_moves[(7, j)] = "black queen"
          possible_moves[(7, j)] = "black bishop"
          possible_moves[(7, j)] = "black rook"
          possible_moves[(7, j)] = "black knight"

        # Check if both spaces are available to move
        elif i == 1:
          possible_moves[(i + 1, j)] = "black pawn"
          if piece_names[i + 2, j] == "":
            possible_moves[(i + 2, j)] = "black pawn"

        else:
          possible_moves[(i + 1, j)] = "black pawn"

      # Check if there is a piece diagonally that the pawn can take
      if j > 0:
        if piece_names[i + 1, j - 1][0: 5] == "white":
          possible_moves[(i + 1, j - 1)] = "black pawn"
         
      if j < 7:
        if piece_names[i + 1, j + 1][0: 5] == "white":
          possible_moves[(i + 1, j + 1)] = "black pawn"

    if name == "black rook":
      # Check up
      record_i = i
      record_j = j

      while i < 7:
        if piece_names[i + 1, j][0: 5] == "":
          possible_moves[(i + 1, j)] = "black rook"

        if piece_names[i + 1, j][0: 5] == "white":
          possible_moves[(i + 1, j)] = "black rook"
          break

        if piece_names[i + 1, j][0: 5] == "black":
          break

        i += 1

      i = record_i
      # Check down
      while i > 0:
        if piece_names[i - 1, j][0: 5] == "":
          possible_moves[(i - 1, j)] = "black rook"

        if piece_names[i - 1, j][0: 5] == "white":
          possible_moves[(i - 1, j)] = "black rook"
          break

        if piece_names[i - 1, j][0: 5] == "black":
          break

        i -= 1

      i = record_i
      # Check left
      while j > 0:
        if piece_names[i, j - 1][0: 5] == "":
          possible_moves[(i, j - 1)] = "black rook"

        if piece_names[i, j - 1][0: 5] == "white":
          possible_moves[(i, j - 1)] = "black rook"
          break

        if piece_names[i, j - 1][0: 5] == "black":
          break

        j -= 1

      j = record_j
      # Check right
      while j < 7:
        if piece_names[i, j + 1][0: 5] == "":
          possible_moves[(i, j + 1)] = "black rook"

        if piece_names[i, j + 1][0: 5] == "white":
          possible_moves[(i, j + 1)] = "black rook"
          break

        if piece_names[i, j + 1][0: 5] == "black":
          break

        j += 1

    if name == "black bishop":
      # Check up
      record_i = i
      record_j = j

      while i < 7 and j < 7:
        if piece_names[i + 1, j + 1][0: 5] == "":
          possible_moves[(i + 1, j + 1)] = "black bishop"

        if piece_names[i + 1, j + 1][0: 5] == "white":
          possible_moves[(i + 1, j + 1)] = "black bishop"
          break

        if piece_names[i + 1, j + 1][0: 5] == "black":
          break

        i += 1
        j += 1

      i = record_i
      j = record_j

      while i < 7 and j > 0:
        if piece_names[i + 1, j - 1][0: 5] == "":
          possible_moves[(i + 1, j - 1)] = "black bishop"

        if piece_names[i + 1, j - 1][0: 5] == "white":
          possible_moves[(i + 1, j - 1)] = "black bishop"
          break

        if piece_names[i + 1, j - 1][0: 5] == "black":
          break

        i += 1
        j -= 1

      i = record_i
      j = record_j

      while i > 0 and j > 0:
        if piece_names[i - 1, j - 1][0: 5] == "":
          possible_moves[(i - 1, j - 1)] = "black bishop"

        if piece_names[i - 1, j - 1][0: 5] == "white":
          possible_moves[(i - 1, j - 1)] = "black bishop"
          break

        if piece_names[i - 1, j - 1][0: 5] == "black":
          break

        i -= 1
        j -= 1

      i = record_i
      j = record_j

      while i > 0 and j < 7:
        if piece_names[i - 1, j + 1][0: 5] == "":
          possible_moves[(i - 1, j + 1)] = "black bishop"

        if piece_names[i - 1, j + 1][0: 5] == "white":
          possible_moves[(i - 1, j + 1)] = "black bishop"
          break

        if piece_names[i - 1, j + 1][0: 5] == "black":
          break

        i -= 1
        j += 1

      i = record_i
      j = record_j

    if name == "black queen":
      possible_moves = piece_moves("black rook", position, piece_names,
                                   next_move)
      possible_moves2 = piece_moves("black bishop", position, piece_names,
                                    next_move)
      possible_moves.update(possible_moves2)

    if name == "black king":
      for i_ in range(max(i - 1, 0), min(i + 1, 7) + 1):
        for j_ in range(max(j - 1, 0), min(j + 1, 7) + 1):
          if piece_names[i_, j_][0: 5] != "black":
            possible_moves[(i_, j_)] = "black king"

    if name == "black knight":
      locations = [[i - 1, j - 2], [i + 1, j - 2], [i - 1, j + 2],
                   [i + 1, j + 2], [i - 2, j - 1], [i - 2, j + 1],
                   [i + 2, j - 1], [i + 2, j + 1]]

      for location in locations:
        i_, j_ = location[0], location[1]

        if (i_ >= 0) and (i_ <= 7):
          if (j_ >= 0) and (j_ <= 7):
            if piece_names[i_, j_][0: 5] != "black":
              possible_moves[(i_, j_)] = "black knight"

  return possible_moves
