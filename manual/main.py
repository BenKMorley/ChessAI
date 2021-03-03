from chessboard.chessboard import Chessboard
from chessboard.encoding.encoding import fen_to_chessboard

OPT = 'qt'

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
game = Chessboard()
fen_to_chessboard(game, STARTING_FEN)


if OPT == 'tk':
    from renderer.tk.tk_renderer import display as tk_display
    tk_display(game)

if OPT == 'qt':
    from renderer.qt5.qt5_renderer import display as qt_display
    qt_display(game)

if OPT == 'mpl':
    from renderer.mpl.mpl_renderer import display as mpl_display
    mpl_display(game)
